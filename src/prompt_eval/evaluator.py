"""Core evaluator engine for running prompt evaluations.

INTERNAL MODULE: This evaluator is used internally by the CLI.
Users should run evaluations via CLI commands, not instantiate this class directly.
"""

import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Callable

from anthropic import Anthropic
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table

from prompt_eval.models import Prompt, TestCase, EvalResult, EvalRun
from prompt_eval.metrics import Metric, Contains


class Evaluator:
    """Main evaluation engine for running prompt tests."""
    
    def __init__(
        self,
        evaluation_threshold: float,
        model: str = "claude-opus-4-5-20251101",
        client: Anthropic | None = None,
        max_tokens: int = 1024,
        temperature: float = 0.0,
        verbose: bool = True,
    ):
        self.model = model
        self.client = client or Anthropic()
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.evaluation_threshold = evaluation_threshold
        self.verbose = verbose
        self.console = Console()
    
    def evaluate_single(
        self,
        prompt: Prompt,
        test_case: TestCase,
        metrics: list[Metric] | None = None,
    ) -> EvalResult:
        """Evaluate a single test case against a prompt."""

        metrics = metrics or [Contains()]

        # Build the complete system prompt with rules, skills, etc.
        system_prompt = prompt.build_system_prompt()

        # Build the complete user prompt with examples and template
        user_prompt = prompt.build_user_prompt(test_case.inputs)

        # Build messages
        messages = [{"role": "user", "content": user_prompt}]

        # Build system blocks with prompt caching for cached files
        cached_files = prompt.get_cached_file_contents()
        if cached_files:
            # Use prompt caching: system is a list of blocks with cache_control
            # IMPORTANT: Anthropic API allows max 4 cache_control blocks
            # So we combine all cached files into a single block
            system_blocks = [
                {
                    "type": "text",
                    "text": system_prompt,
                }
            ]

            # Combine all cached files into a single text block with caching
            all_files_text = []
            for file_info in cached_files:
                file_name = Path(file_info["path"]).name
                all_files_text.append(f"<reference_material file=\"{file_name}\">\n{file_info['content']}\n</reference_material>")

            system_blocks.append({
                "type": "text",
                "text": "\n\n" + "\n\n".join(all_files_text),
                "cache_control": {"type": "ephemeral"}
            })
        else:
            # No caching needed - use simple string
            system_blocks = system_prompt

        # Call the API
        start_time = time.perf_counter()
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_blocks,
                messages=messages,
            )
            latency_ms = (time.perf_counter() - start_time) * 1000

            output = response.content[0].text
            tokens_in = response.usage.input_tokens
            tokens_out = response.usage.output_tokens
            error = None

            # Log cache performance if available
            if self.verbose and hasattr(response.usage, 'cache_creation_input_tokens'):
                if response.usage.cache_creation_input_tokens:
                    self.console.print(f"[dim]Cache created: {response.usage.cache_creation_input_tokens} tokens[/dim]")
                if hasattr(response.usage, 'cache_read_input_tokens') and response.usage.cache_read_input_tokens:
                    self.console.print(f"[dim green]Cache hit: {response.usage.cache_read_input_tokens} tokens saved[/dim green]")

        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000
            output = ""
            tokens_in = 0
            tokens_out = 0
            error = str(e)
        
        # Calculate metrics
        metric_scores = {}
        for metric in metrics:
            try:
                metric_scores[metric.name] = metric.score(output, test_case)
            except Exception as e:
                metric_scores[metric.name] = 0.0
                if self.verbose:
                    self.console.print(f"[yellow]Warning: Metric {metric.name} failed: {e}[/yellow]")
        
        # Determine pass/fail (all metrics must pass with >= evaluation_threshold)
        passed = all(score >= self.evaluation_threshold for score in metric_scores.values()) and error is None
        
        return EvalResult(
            test_case=test_case.name,
            prompt_name=prompt.name,
            system_prompt=system_prompt,
            input_text=user_prompt,
            output=output,
            metrics=metric_scores,
            passed=passed,
            latency_ms=latency_ms,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            error=error,
        )
    
    def evaluate(
        self,
        prompt: Prompt,
        test_cases: list[TestCase],
        metrics: list[Metric] | None = None,
        tags: list[str] | None = None,
        on_result: Callable[[EvalResult], None] | None = None,
    ) -> EvalRun:
        """
        Run a full evaluation of a prompt against multiple test cases.
        
        Args:
            prompt: The prompt to evaluate
            test_cases: List of test cases to run
            metrics: Metrics to calculate (default: Contains)
            tags: Optional filter to only run test cases with these tags
            on_result: Optional callback for each result
        
        Returns:
            EvalRun with all results
        """
        
        # Filter by tags if specified
        if tags:
            test_cases = [tc for tc in test_cases if any(t in tc.tags for t in tags)]
        
        run = EvalRun(
            run_id=str(uuid.uuid4())[:8],
            prompt_name=prompt.name,
            model=self.model,
            config={
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "evaluation_threshold": self.evaluation_threshold,
            }
        )
        
        if self.verbose:
            self.console.print(f"\n[bold blue]Starting evaluation run: {run.run_id}[/bold blue]")
            self.console.print(f"Prompt: {prompt.name} | Model: {self.model} | Tests: {len(test_cases)}\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console,
            disable=not self.verbose,
        ) as progress:
            task = progress.add_task("Evaluating...", total=len(test_cases))
            
            for test_case in test_cases:
                progress.update(task, description=f"Testing: {test_case.name[:30]}")
                
                result = self.evaluate_single(prompt, test_case, metrics)
                run.results.append(result)
                
                if on_result:
                    on_result(result)
                
                progress.advance(task)
        
        run.completed_at = datetime.now()
        
        if self.verbose:
            self.print_summary(run)
        
        return run
    
    def print_summary(self, run: EvalRun) -> None:
        """Print a formatted summary of the evaluation run."""
        
        summary = run.summary()
        
        # Summary table
        table = Table(title=f"Evaluation Summary: {run.run_id}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Prompt", summary["prompt"])
        table.add_row("Model", summary["model"])
        table.add_row("Total Tests", str(summary["total_tests"]))
        table.add_row("Passed", f"[green]{summary['passed']}[/green]")
        table.add_row("Failed", f"[red]{summary['failed']}[/red]")
        table.add_row("Pass Rate", summary["pass_rate"])
        table.add_row("Avg Latency", f"{summary['avg_latency_ms']} ms")
        table.add_row("Total Tokens", str(summary["total_tokens"]))
        
        self.console.print(table)
        
        # Show failures if any
        failures = [r for r in run.results if not r.passed]
        if failures:
            self.console.print("\n[bold red]Failed Tests:[/bold red]")
            for result in failures:
                self.console.print(f"  • {result.test_case}")
                if result.error:
                    self.console.print(f"    [red]Error: {result.error}[/red]")
                else:
                    self.console.print(f"    Metrics: {result.metrics}")
    
    def compare(
        self,
        prompts: list[Prompt],
        test_cases: list[TestCase],
        metrics: list[Metric] | None = None,
    ) -> list[EvalRun]:
        """
        Compare multiple prompts against the same test cases.
        
        Returns a list of EvalRun objects, one for each prompt.
        """
        runs = []
        
        for prompt in prompts:
            if self.verbose:
                self.console.print(f"\n[bold]Evaluating prompt: {prompt.name}[/bold]")
            run = self.evaluate(prompt, test_cases, metrics)
            runs.append(run)
        
        if self.verbose:
            self.print_comparison(runs)
        
        return runs
    
    def print_comparison(self, runs: list[EvalRun]) -> None:
        """Print a comparison table of multiple evaluation runs."""
        
        table = Table(title="Prompt Comparison")
        table.add_column("Prompt", style="cyan")
        table.add_column("Pass Rate", justify="right")
        table.add_column("Avg Latency", justify="right")
        table.add_column("Tokens", justify="right")
        
        for run in runs:
            summary = run.summary()
            table.add_row(
                run.prompt_name,
                summary["pass_rate"],
                f"{summary['avg_latency_ms']} ms",
                str(summary["total_tokens"]),
            )
        
        self.console.print("\n")
        self.console.print(table)
