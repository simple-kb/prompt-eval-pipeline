"""Command-line interface for the prompt evaluation pipeline."""

import click
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console

# Load .env file
load_dotenv()

from prompt_eval.evaluator import Evaluator
from prompt_eval.loaders import load_eval_config
from prompt_eval.exporters import ResultsExporter, compare_runs_to_markdown
from prompt_eval.metrics import Contains, ExactMatch, LLMJudge, ResponseLength


console = Console()


def build_metrics(metrics_config: list[dict]) -> list:
    """Build metric instances from configuration."""
    metrics = []
    
    for config in metrics_config:
        metric_type = config.get("type", "contains")
        
        if metric_type == "contains":
            metrics.append(Contains(
                case_sensitive=config.get("case_sensitive", False)
            ))
        elif metric_type == "exact_match":
            metrics.append(ExactMatch(
                case_sensitive=config.get("case_sensitive", False),
                strip=config.get("strip", True)
            ))
        elif metric_type == "llm_judge":
            metrics.append(LLMJudge(
                criteria=config.get("criteria", "Is the response helpful and accurate?"),
                model=config.get("model", "claude-sonnet-4-20250514")
            ))
        elif metric_type == "response_length":
            metrics.append(ResponseLength(
                min_chars=config.get("min_chars", 0),
                max_chars=config.get("max_chars"),
                min_words=config.get("min_words", 0),
                max_words=config.get("max_words")
            ))
    
    return metrics or [Contains()]


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Prompt Evaluation Pipeline - Test and compare LLM prompts."""
    pass


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output directory for results")
@click.option("--format", "-f", type=click.Choice(["json", "csv", "markdown", "html", "all"]), 
              default="all", help="Output format")
@click.option("--model", "-m", help="Override model from config")
@click.option("--verbose/--quiet", "-v/-q", default=True, help="Verbose output")
def run(config_file: str, output: str | None, format: str, model: str | None, verbose: bool):
    """Run evaluation from a config file."""
    
    console.print(f"[bold]Loading config from {config_file}...[/bold]")
    config = load_eval_config(config_file)
    
    # Override model if specified
    if model:
        config["model"] = model
    
    # Build evaluator
    evaluator = Evaluator(
        model=config["model"],
        max_tokens=config["max_tokens"],
        temperature=config["temperature"],
        verbose=verbose,
    )
    
    # Build metrics
    metrics = build_metrics(config.get("metrics_config", []))
    
    # Get prompts and test cases
    prompts = config.get("prompts", [])
    test_cases = config.get("test_cases", [])
    
    if not prompts:
        console.print("[red]No prompts found in config![/red]")
        return
    
    if not test_cases:
        console.print("[red]No test cases found in config![/red]")
        return
    
    # Run evaluations
    runs = []
    for prompt in prompts:
        run_result = evaluator.evaluate(prompt, test_cases, metrics)
        runs.append(run_result)
    
    # Export results
    output_dir = output or "results"
    exporter = ResultsExporter(output_dir)
    
    for run_result in runs:
        if format == "all":
            paths = exporter.export_all(run_result)
            console.print(f"\n[green]Results exported to:[/green]")
            for fmt, path in paths.items():
                console.print(f"  {fmt}: {path}")
        else:
            export_method = getattr(exporter, f"to_{format}")
            path = export_method(run_result)
            console.print(f"\n[green]Results exported to: {path}[/green]")
    
    # Create comparison if multiple prompts
    if len(runs) > 1:
        comparison_path = Path(output_dir) / "comparison.md"
        compare_runs_to_markdown(runs, comparison_path)
        console.print(f"[green]Comparison report: {comparison_path}[/green]")


if __name__ == "__main__":
    main()
