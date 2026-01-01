"""Export evaluation results to various formats.

INTERNAL MODULE: Exporters are used internally by the CLI.
Users don't need to interact with this module - results are exported automatically by CLI commands.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from prompt_eval.models import EvalRun, EvalResult


class ResultsExporter:
    """Export evaluation results to various formats (internal use only)."""
    
    def __init__(self, output_dir: str | Path = "results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_filename(self, run: EvalRun, extension: str) -> Path:
        """Generate a filename for the export."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.output_dir / f"{run.prompt_name}_{run.run_id}_{timestamp}.{extension}"
    
    def to_json(self, run: EvalRun, path: str | Path | None = None) -> Path:
        """Export results to JSON."""
        path = Path(path) if path else self._generate_filename(run, "json")
        
        data = {
            "run_id": run.run_id,
            "prompt_name": run.prompt_name,
            "model": run.model,
            "config": run.config,
            "started_at": run.started_at.isoformat(),
            "completed_at": run.completed_at.isoformat() if run.completed_at else None,
            "summary": run.summary(),
            "results": [r.model_dump() for r in run.results],
        }
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        
        return path
    
    def to_csv(self, run: EvalRun, path: str | Path | None = None) -> Path:
        """Export results to CSV."""
        path = Path(path) if path else self._generate_filename(run, "csv")
        
        rows = []
        for result in run.results:
            row = {
                "run_id": run.run_id,
                "prompt_name": result.prompt_name,
                "test_case": result.test_case,
                "passed": result.passed,
                "latency_ms": result.latency_ms,
                "tokens_in": result.tokens_in,
                "tokens_out": result.tokens_out,
                "error": result.error,
            }
            # Flatten metrics
            for metric_name, score in result.metrics.items():
                row[f"metric_{metric_name}"] = score
            rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_csv(path, index=False)
        
        return path
    
    def to_markdown(self, run: EvalRun, path: str | Path | None = None) -> Path:
        """Export results to Markdown report."""
        path = Path(path) if path else self._generate_filename(run, "md")
        
        summary = run.summary()
        
        lines = [
            f"# Evaluation Report: {run.prompt_name}",
            "",
            f"**Run ID:** {run.run_id}",
            f"**Model:** {run.model}",
            f"**Date:** {run.started_at.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Tests | {summary['total_tests']} |",
            f"| Passed | {summary['passed']} |",
            f"| Failed | {summary['failed']} |",
            f"| Pass Rate | {summary['pass_rate']} |",
            f"| Avg Latency | {summary['avg_latency_ms']} ms |",
            f"| Total Tokens | {summary['total_tokens']} |",
            "",
            "## Results",
            "",
        ]
        
        # Results table
        lines.append("| Test Case | Passed | Latency (ms) | Metrics |")
        lines.append("|-----------|--------|--------------|---------|")
        
        for result in run.results:
            status = "✅" if result.passed else "❌"
            metrics_str = ", ".join(f"{k}={v:.2f}" for k, v in result.metrics.items())
            lines.append(f"| {result.test_case} | {status} | {result.latency_ms:.0f} | {metrics_str} |")
        
        # Test details for all tests
        lines.extend([
            "",
            "## Test Details",
            "",
        ])
        for result in run.results:
            status_icon = "✅" if result.passed else "❌"
            lines.extend([
                f"### {result.test_case} {status_icon}",
                "",
                "**System Prompt:**",
                "```",
                result.system_prompt,
                "```",
                "",
                "**Input:**",
                "```",
                result.input_text,
                "```",
                "",
                "**Output:**",
                "```",
                result.output,
                "```",
                "",
                f"**Metrics:** {result.metrics}",
                "",
            ])
            if result.error:
                lines.append(f"**Error:** {result.error}")
                lines.append("")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        return path
    
    def to_html(self, run: EvalRun, path: str | Path | None = None) -> Path:
        """Export results to HTML report."""
        path = Path(path) if path else self._generate_filename(run, "html")
        
        summary = run.summary()
        
        # Build HTML
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Eval Report: {run.prompt_name}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
        .metric {{ text-align: center; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #2563eb; }}
        .metric-label {{ color: #666; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f9fafb; }}
        .pass {{ color: #22c55e; }}
        .fail {{ color: #ef4444; }}
        .details {{ background: #fefefe; border: 1px solid #e5e7eb; padding: 15px; margin: 10px 0; border-radius: 4px; }}
        pre {{ background: #f3f4f6; padding: 10px; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; overflow-wrap: break-word; }}
    </style>
</head>
<body>
    <h1>Evaluation Report: {run.prompt_name}</h1>
    <p><strong>Run ID:</strong> {run.run_id} | <strong>Model:</strong> {run.model} | <strong>Date:</strong> {run.started_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="summary">
        <div class="summary-grid">
            <div class="metric">
                <div class="metric-value">{summary['pass_rate']}</div>
                <div class="metric-label">Pass Rate</div>
            </div>
            <div class="metric">
                <div class="metric-value">{summary['passed']}/{summary['total_tests']}</div>
                <div class="metric-label">Tests Passed</div>
            </div>
            <div class="metric">
                <div class="metric-value">{summary['avg_latency_ms']} ms</div>
                <div class="metric-label">Avg Latency</div>
            </div>
        </div>
    </div>
    
    <h2>Results</h2>
    <table>
        <thead>
            <tr>
                <th>Test Case</th>
                <th>Status</th>
                <th>Latency</th>
                <th>Tokens In</th>
                <th>Tokens Out</th>
                <th>Metrics</th>
            </tr>
        </thead>
        <tbody>
"""

        for result in run.results:
            status_class = "pass" if result.passed else "fail"
            status_icon = "✅" if result.passed else "❌"
            metrics_str = ", ".join(f"{k}={v:.2f}" for k, v in result.metrics.items())

            html += f"""            <tr>
                <td>{result.test_case}</td>
                <td class="{status_class}">{status_icon}</td>
                <td>{result.latency_ms:.0f} ms</td>
                <td>{result.tokens_in}</td>
                <td>{result.tokens_out}</td>
                <td>{metrics_str}</td>
            </tr>
"""
        
        html += """        </tbody>
    </table>
"""
        
        # Add test details for all tests
        html += """    <h2>Test Details</h2>
"""
        for result in run.results:
            html += f"""    <div class="details">
        <h3>{result.test_case} {'✅' if result.passed else '❌'}</h3>
        <p><strong>System Prompt:</strong></p>
        <pre>{result.system_prompt}</pre>
        <p><strong>Input:</strong></p>
        <pre>{result.input_text}</pre>
        <p><strong>Output:</strong></p>
        <pre>{result.output}</pre>
        <p><strong>Metrics:</strong> {result.metrics}</p>
"""
            if result.error:
                html += f"""        <p><strong>Error:</strong> {result.error}</p>
"""
            html += """    </div>
"""
        
        html += """</body>
</html>"""
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        
        return path
    
    def export_all(self, run: EvalRun) -> dict[str, Path]:
        """Export to all formats."""
        return {
            "json": self.to_json(run),
            "csv": self.to_csv(run),
            "markdown": self.to_markdown(run),
            "html": self.to_html(run),
        }


def compare_runs_to_markdown(runs: list[EvalRun], path: str | Path) -> Path:
    """Create a comparison report for multiple evaluation runs."""
    path = Path(path)
    
    lines = [
        "# Prompt Comparison Report",
        "",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Prompts Compared:** {len(runs)}",
        "",
        "## Summary Comparison",
        "",
        "| Prompt | Pass Rate | Avg Latency | Total Tokens |",
        "|--------|-----------|-------------|--------------|",
    ]
    
    for run in runs:
        summary = run.summary()
        lines.append(f"| {run.prompt_name} | {summary['pass_rate']} | {summary['avg_latency_ms']} ms | {summary['total_tokens']} |")
    
    lines.extend([
        "",
        "## Test-by-Test Comparison",
        "",
    ])
    
    # Get all test case names
    all_tests = set()
    for run in runs:
        for result in run.results:
            all_tests.add(result.test_case)
    
    # Build comparison table
    header = "| Test Case | " + " | ".join(r.prompt_name for r in runs) + " |"
    separator = "|-----------|" + "|".join("-" * (len(r.prompt_name) + 2) for r in runs) + "|"
    lines.extend([header, separator])
    
    for test_name in sorted(all_tests):
        row = [test_name]
        for run in runs:
            result = next((r for r in run.results if r.test_case == test_name), None)
            if result:
                row.append("✅" if result.passed else "❌")
            else:
                row.append("-")
        lines.append("| " + " | ".join(row) + " |")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    return path
