"""Evaluation metrics for comparing model outputs against expectations.

INTERNAL MODULE: These metrics are used internally by the CLI.
Users should configure metrics in YAML files using the 'type' field, not instantiate these classes directly.
"""

from abc import ABC, abstractmethod
import re
from anthropic import Anthropic


class Metric(ABC):
    """Base class for evaluation metrics."""
    
    name: str = "base_metric"
    
    @abstractmethod
    def score(self, output: str, test_case: "TestCase") -> float:
        """
        Score the output against the test case expectations.
        
        Returns a float between 0.0 and 1.0.
        """
        pass
    
    def passes(self, output: str, test_case: "TestCase", threshold: float = 0.5) -> bool:
        """Check if the output passes based on the threshold."""
        return self.score(output, test_case) >= threshold


class ExactMatch(Metric):
    """Check if output exactly matches expected value."""
    
    name = "exact_match"
    
    def __init__(self, case_sensitive: bool = False, strip: bool = True):
        self.case_sensitive = case_sensitive
        self.strip = strip
    
    def score(self, output: str, test_case) -> float:
        if test_case.expected is None:
            return 1.0  # No expectation = pass
        
        expected = test_case.expected
        actual = output
        
        if self.strip:
            expected = expected.strip()
            actual = actual.strip()
        
        if not self.case_sensitive:
            expected = expected.lower()
            actual = actual.lower()
        
        return 1.0 if expected == actual else 0.0


class Contains(Metric):
    """Check if output contains expected substrings."""
    
    name = "contains"
    
    def __init__(self, case_sensitive: bool = False):
        self.case_sensitive = case_sensitive
    
    def score(self, output: str, test_case) -> float:
        if not test_case.expected_contains and not test_case.expected_not_contains:
            return 1.0  # No expectations = pass
        
        check_output = output if self.case_sensitive else output.lower()
        
        # Check required substrings
        contains_score = 1.0
        if test_case.expected_contains:
            matches = 0
            for substring in test_case.expected_contains:
                check_sub = substring if self.case_sensitive else substring.lower()
                if check_sub in check_output:
                    matches += 1
            contains_score = matches / len(test_case.expected_contains)
        
        # Check forbidden substrings
        not_contains_score = 1.0
        if test_case.expected_not_contains:
            violations = 0
            for substring in test_case.expected_not_contains:
                check_sub = substring if self.case_sensitive else substring.lower()
                if check_sub in check_output:
                    violations += 1
            not_contains_score = 1.0 - (violations / len(test_case.expected_not_contains))
        
        # Both must pass
        return min(contains_score, not_contains_score)


class ResponseLength(Metric):
    """Check if response length is within expected bounds."""
    
    name = "response_length"
    
    def __init__(self, min_chars: int = 0, max_chars: int | None = None, 
                 min_words: int = 0, max_words: int | None = None):
        self.min_chars = min_chars
        self.max_chars = max_chars
        self.min_words = min_words
        self.max_words = max_words
    
    def score(self, output: str, test_case) -> float:
        char_count = len(output)
        word_count = len(output.split())
        
        # Check character bounds
        if char_count < self.min_chars:
            return 0.0
        if self.max_chars and char_count > self.max_chars:
            return 0.0
        
        # Check word bounds
        if word_count < self.min_words:
            return 0.0
        if self.max_words and word_count > self.max_words:
            return 0.0
        
        return 1.0


class RegexMatch(Metric):
    """Check if output matches a regex pattern."""
    
    name = "regex_match"
    
    def __init__(self, pattern: str, flags: int = 0):
        self.pattern = re.compile(pattern, flags)
    
    def score(self, output: str, test_case) -> float:
        return 1.0 if self.pattern.search(output) else 0.0


class LLMJudge(Metric):
    """Use an LLM to judge the quality of the output."""
    
    name = "llm_judge"
    
    def __init__(
        self, 
        criteria: str = "Is the response helpful, accurate, and well-formatted?",
        model: str = "claude-sonnet-4-20250514",
        client: Anthropic | None = None
    ):
        self.criteria = criteria
        self.model = model
        self.client = client or Anthropic()
    
    def score(self, output: str, test_case) -> float:
        # Build the judging prompt
        judge_prompt = f"""You are evaluating an AI assistant's response.

TASK/INPUT:
{test_case.inputs}

AI RESPONSE:
{output}

EVALUATION CRITERIA:
{self.criteria}

Score the response from 0.0 to 1.0, where:
- 0.0 = Completely fails the criteria
- 0.5 = Partially meets the criteria
- 1.0 = Fully meets the criteria

Respond with ONLY a number between 0.0 and 1.0, nothing else."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": judge_prompt}]
            )
            score_text = response.content[0].text.strip()
            return float(score_text)
        except (ValueError, IndexError):
            return 0.5  # Default to middle score on parse failure


class CompositeMetric(Metric):
    """Combine multiple metrics with weights."""
    
    name = "composite"
    
    def __init__(self, metrics: list[tuple[Metric, float]]):
        """
        Args:
            metrics: List of (metric, weight) tuples
        """
        self.metrics = metrics
        total_weight = sum(w for _, w in metrics)
        # Normalize weights
        self.metrics = [(m, w / total_weight) for m, w in metrics]
    
    def score(self, output: str, test_case) -> float:
        total = 0.0
        for metric, weight in self.metrics:
            total += metric.score(output, test_case) * weight
        return total
