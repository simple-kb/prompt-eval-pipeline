"""Export evaluation results to various formats.

INTERNAL MODULE: Exporters are used internally by the CLI.
Users don't need to interact with this module - results are exported automatically by CLI commands.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from prompt_eval.models import EvalRun, EvalResult


def _convert_markdown_tables_to_html(
    text: str,
    expected_functions: set[str] | None = None,
    confidence_threshold: float | None = None
) -> str:
    """Convert markdown tables in text to HTML tables and apply basic markdown formatting.

    Searches for markdown table patterns and converts them to HTML.
    Also converts basic markdown elements like headings, bold text, and lists.

    Args:
        text: The markdown text to convert
        expected_functions: Set of function numbers (e.g., {"01", "08", "09"}) for highlighting
        confidence_threshold: Threshold for determining correct/incorrect (e.g., 0.85)
    """
    # Pattern to match markdown tables
    # Matches: header row | separator row | data rows
    table_pattern = r'(\|[^\n]+\|\n\|[\s\-:|]+\|\n(?:\|[^\n]+\|\n?)+)'

    def convert_table(match):
        table_md = match.group(1)
        lines = [line.strip() for line in table_md.strip().split('\n') if line.strip()]

        if len(lines) < 2:
            return table_md  # Not a valid table

        # Parse header
        header_cells = [cell.strip() for cell in lines[0].split('|')[1:-1]]

        # Find column indices dynamically based on header names
        # Support both English and French headers
        function_col_idx = None
        confidence_col_idx = None
        for idx, header in enumerate(header_cells):
            header_lower = header.lower()
            if 'function' in header_lower or 'fonction' in header_lower:
                function_col_idx = idx
            elif 'confidence' in header_lower or 'confiance' in header_lower:
                confidence_col_idx = idx

        # Check if this is a details table with Function Name and Confidence columns
        is_details_table = (
            expected_functions is not None
            and confidence_threshold is not None
            and function_col_idx is not None
            and confidence_col_idx is not None
        )

        # Skip separator line (lines[1])

        # Parse data rows
        data_rows = []
        for line in lines[2:]:
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if cells:  # Skip empty rows
                data_rows.append(cells)

        # Build HTML table
        html = '<table>\n'
        html += '  <thead>\n    <tr>\n'
        for cell in header_cells:
            html += f'      <th>{cell}</th>\n'
        html += '    </tr>\n  </thead>\n'
        html += '  <tbody>\n'
        for row in data_rows:
            row_class = ""

            # Apply highlighting for details table
            if is_details_table and len(row) > max(function_col_idx, confidence_col_idx):
                # Extract function number from function column (e.g., "01. Absentation" -> "01")
                func_match = re.match(r'^(\d+)', row[function_col_idx])
                if func_match:
                    func_num = func_match.group(1)

                    # Extract confidence score from confidence column
                    try:
                        confidence = float(row[confidence_col_idx])
                        is_in_expected = func_num in expected_functions
                        is_above_threshold = confidence >= confidence_threshold

                        if is_above_threshold and is_in_expected:
                            row_class = ' class="row-correct"'  # True positive - green
                        elif is_above_threshold and not is_in_expected:
                            row_class = ' class="row-incorrect"'  # False positive - red
                        elif not is_above_threshold and is_in_expected:
                            row_class = ' class="row-incorrect"'  # False negative - red
                        # else: True negative - no highlight
                    except (ValueError, IndexError):
                        pass  # Can't parse confidence, skip highlighting

            html += f'    <tr{row_class}>\n'
            for cell in row:
                html += f'      <td>{cell}</td>\n'
            html += '    </tr>\n'
        html += '  </tbody>\n'
        html += '</table>'

        return html

    # Replace all markdown tables with HTML tables
    result = re.sub(table_pattern, convert_table, text, flags=re.MULTILINE)

    # Convert other markdown elements
    # Headings (# to ######)
    result = re.sub(r'^######\s+(.+)$', r'<h6>\1</h6>', result, flags=re.MULTILINE)
    result = re.sub(r'^#####\s+(.+)$', r'<h5>\1</h5>', result, flags=re.MULTILINE)
    result = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', result, flags=re.MULTILINE)
    result = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', result, flags=re.MULTILINE)
    result = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', result, flags=re.MULTILINE)
    result = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', result, flags=re.MULTILINE)

    # Bold text (**text** or __text__)
    result = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', result)
    result = re.sub(r'__(.+?)__', r'<strong>\1</strong>', result)

    # Italic text (*text* or _text_)
    result = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', result)
    result = re.sub(r'(?<!_)_(?!_)(.+?)(?<!_)_(?!_)', r'<em>\1</em>', result)

    # Bullet lists (- item)
    result = re.sub(r'^-\s+(.+)$', r'<li>\1</li>', result, flags=re.MULTILINE)

    # Wrap consecutive <li> elements in <ul>
    result = re.sub(r'(<li>.*?</li>(?:\s*<li>.*?</li>)*)', r'<ul>\1</ul>', result, flags=re.DOTALL)

    # Horizontal rules (---)
    result = re.sub(r'^---+$', r'<hr>', result, flags=re.MULTILINE)

    # Convert line breaks to <br> for proper formatting
    result = re.sub(r'\n\n', '<br><br>', result)

    return result


def _highlight_html_tables(
    text: str,
    expected_functions: set[str] | None = None,
    confidence_threshold: float | None = None
) -> str:
    """Add row highlighting to existing HTML tables in text.

    Searches for HTML table patterns and adds row-correct/row-incorrect classes
    based on function matching and confidence scores.

    Args:
        text: The HTML text containing tables
        expected_functions: Set of function numbers (e.g., {"01", "08", "09"}) for highlighting
        confidence_threshold: Threshold for determining correct/incorrect (e.g., 0.85)
    """
    if expected_functions is None or confidence_threshold is None:
        return text

    # Pattern to match HTML tables
    table_pattern = r'<table[^>]*>.*?</table>'

    def process_table(match):
        table_html = match.group(0)

        # Find header row to identify column indices
        header_match = re.search(r'<thead[^>]*>(.*?)</thead>', table_html, re.DOTALL)
        if not header_match:
            return table_html

        header_content = header_match.group(1)
        # Extract header cells
        header_cells = re.findall(r'<th[^>]*>(.*?)</th>', header_content, re.DOTALL)

        # Find column indices dynamically based on header names
        # Support both English and French headers
        function_col_idx = None
        confidence_col_idx = None
        for idx, header in enumerate(header_cells):
            header_lower = header.lower()
            if 'function' in header_lower or 'fonction' in header_lower:
                function_col_idx = idx
            elif 'confidence' in header_lower or 'confiance' in header_lower:
                confidence_col_idx = idx

        # If we can't find the right columns, return unchanged
        if function_col_idx is None or confidence_col_idx is None:
            return table_html

        # Process each row in tbody
        def process_row(row_match):
            row_html = row_match.group(0)

            # Extract cells from the row
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)

            if len(cells) <= max(function_col_idx, confidence_col_idx):
                return row_html

            # Extract function number from function column (e.g., "01. Éloignement" -> "01")
            # Also handle <strong>01. Éloignement</strong> format
            func_text = re.sub(r'<[^>]+>', '', cells[function_col_idx])  # Remove HTML tags
            func_match = re.match(r'^\s*(\d+)', func_text)
            if not func_match:
                return row_html

            func_num = func_match.group(1)

            # Extract confidence score from confidence column
            conf_text = re.sub(r'<[^>]+>', '', cells[confidence_col_idx])  # Remove HTML tags
            try:
                confidence = float(conf_text.strip())
            except ValueError:
                return row_html

            is_in_expected = func_num in expected_functions
            is_above_threshold = confidence >= confidence_threshold

            row_class = ""
            if is_above_threshold and is_in_expected:
                row_class = 'row-correct'  # True positive - green
            elif is_above_threshold and not is_in_expected:
                row_class = 'row-incorrect'  # False positive - red
            elif not is_above_threshold and is_in_expected:
                row_class = 'row-incorrect'  # False negative - red
            # else: True negative - no highlight

            if row_class:
                # Add or update class attribute on <tr>
                if 'class=' in row_html[:20]:
                    # Already has a class, append to it
                    row_html = re.sub(r'<tr([^>]*)\sclass="([^"]*)"', f'<tr\\1 class="\\2 {row_class}"', row_html)
                else:
                    # No class, add one
                    row_html = row_html.replace('<tr>', f'<tr class="{row_class}">', 1)
                    row_html = re.sub(r'<tr\s', f'<tr class="{row_class}" ', row_html, count=1)

            return row_html

        # Process rows in tbody
        tbody_pattern = r'<tbody[^>]*>(.*?)</tbody>'
        tbody_match = re.search(tbody_pattern, table_html, re.DOTALL)
        if tbody_match:
            tbody_content = tbody_match.group(1)
            # Process each <tr>...</tr>
            new_tbody_content = re.sub(r'<tr[^>]*>.*?</tr>', process_row, tbody_content, flags=re.DOTALL)
            table_html = table_html[:tbody_match.start(1)] + new_tbody_content + table_html[tbody_match.end(1):]

        return table_html

    return re.sub(table_pattern, process_table, text, flags=re.DOTALL)


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
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; font-size: 12px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
        .metric {{ text-align: center; }}
        .metric-value {{ font-size: 12px; font-weight: bold; color: #2563eb; }}
        .metric-label {{ color: #666; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f9fafb; }}
        .pass {{ color: #22c55e; }}
        .fail {{ color: #ef4444; }}
        .details {{ background: #fefefe; border: 1px solid #e5e7eb; padding: 15px; margin: 10px 0; border-radius: 4px; }}
        pre {{ background: #f3f4f6; padding: 10px; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; overflow-wrap: break-word; }}
        .row-correct {{ background-color: #dcfce7; }}
        .row-incorrect {{ background-color: #fee2e2; }}
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
            # Extract expected functions and confidence threshold for highlighting
            expected_functions = None
            confidence_threshold = None

            if result.expected_contains and result.test_case_inputs:
                # Parse expected sequence (e.g., "01, 08, 09, 11" -> {"01", "08", "09", "11"})
                if result.expected_contains:
                    expected_seq = result.expected_contains[0] if result.expected_contains else ""
                    expected_functions = {num.strip() for num in expected_seq.split(",")}

                # Get confidence threshold from inputs
                confidence_threshold = result.test_case_inputs.get("confidence_threshold")

            # Convert markdown tables to HTML in the output (with optional highlighting)
            output_html = _convert_markdown_tables_to_html(
                result.output,
                expected_functions=expected_functions,
                confidence_threshold=confidence_threshold
            )
            # Also highlight any HTML tables that the LLM output directly
            output_html = _highlight_html_tables(
                output_html,
                expected_functions=expected_functions,
                confidence_threshold=confidence_threshold
            )

            html += f"""    <div class="details">
        <h3>{result.test_case} {'✅' if result.passed else '❌'}</h3>
        <p><strong>System Prompt:</strong></p>
        <pre>{result.system_prompt}</pre>
        <p><strong>Input:</strong></p>
        <pre>{result.input_text}</pre>
        <p><strong>Output:</strong></p>
        <div>{output_html}</div>
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
