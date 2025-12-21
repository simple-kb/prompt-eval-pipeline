"""Data models for the prompt evaluation pipeline.

INTERNAL MODULE: These models are used internally by the CLI.
Users should define prompts and test cases in YAML files, not instantiate these classes directly.
"""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class Prompt(BaseModel):
    """A prompt template to be evaluated."""
    
    name: str = Field(..., description="Unique identifier for the prompt")
    template: str = Field(..., description="The prompt template with {variable} placeholders")
    system: str | None = Field(None, description="Optional system prompt")
    description: str = Field("", description="Description of what this prompt does")
    version: str = Field("1.0", description="Version of this prompt")
    
    def render(self, variables: dict[str, Any]) -> str:
        """Render the prompt template with the given variables."""
        return self.template.format(**variables)


class TestCase(BaseModel):
    """A single test case for prompt evaluation."""
    
    name: str = Field(..., description="Name/identifier for this test case")
    inputs: dict[str, Any] = Field(..., description="Input variables for the prompt template")
    expected: str | None = Field(None, description="Expected output (for exact match)")
    expected_contains: list[str] = Field(default_factory=list, description="Strings that should appear in output")
    expected_not_contains: list[str] = Field(default_factory=list, description="Strings that should NOT appear")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    tags: list[str] = Field(default_factory=list, description="Tags for filtering test cases")


class EvalResult(BaseModel):
    """Result of evaluating a single test case."""
    
    test_case: str = Field(..., description="Name of the test case")
    prompt_name: str = Field(..., description="Name of the prompt evaluated")
    input_text: str = Field(..., description="The rendered prompt sent to the model")
    output: str = Field(..., description="Model's response")
    metrics: dict[str, float] = Field(default_factory=dict, description="Metric scores")
    passed: bool = Field(..., description="Whether the test passed overall")
    latency_ms: float = Field(..., description="Response time in milliseconds")
    tokens_in: int = Field(0, description="Input token count")
    tokens_out: int = Field(0, description="Output token count")
    error: str | None = Field(None, description="Error message if evaluation failed")
    timestamp: datetime = Field(default_factory=datetime.now)


class EvalRun(BaseModel):
    """A complete evaluation run with multiple test cases."""
    
    run_id: str = Field(..., description="Unique identifier for this run")
    prompt_name: str = Field(..., description="Name of the prompt being evaluated")
    model: str = Field(..., description="Model used for evaluation")
    results: list[EvalResult] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: datetime | None = None
    config: dict[str, Any] = Field(default_factory=dict)
    
    @property
    def pass_rate(self) -> float:
        """Calculate the percentage of tests that passed."""
        if not self.results:
            return 0.0
        return sum(1 for r in self.results if r.passed) / len(self.results)
    
    @property
    def avg_latency_ms(self) -> float:
        """Calculate average latency across all results."""
        if not self.results:
            return 0.0
        return sum(r.latency_ms for r in self.results) / len(self.results)
    
    def summary(self) -> dict[str, Any]:
        """Generate a summary of the evaluation run."""
        return {
            "run_id": self.run_id,
            "prompt": self.prompt_name,
            "model": self.model,
            "total_tests": len(self.results),
            "passed": sum(1 for r in self.results if r.passed),
            "failed": sum(1 for r in self.results if not r.passed),
            "pass_rate": f"{self.pass_rate:.1%}",
            "avg_latency_ms": f"{self.avg_latency_ms:.0f}",
            "total_tokens": sum(r.tokens_in + r.tokens_out for r in self.results),
        }
