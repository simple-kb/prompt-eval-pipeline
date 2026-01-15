# Prompt Evaluation Pipeline

A declarative YAML-based framework for systematically testing and comparing LLM prompts. Define your prompts and test cases in YAML, run evaluations via CLI, and generate detailed reports.

To quickly understand how this project works, review these two files:

* Prompt definition: [prompts/narrative-function-extractor/narrative-function-extractor_v3.yaml](./prompts\narrative-function-extractor\narrative-function-extractor_v3.yaml)
* Sample results: [results/narrative-function-extractor/20260107_114239/narrative-function-extractor_v3_e94a9b0d_20260107_114239.html](./results/narrative-function-extractor/20260107_114239/narrative-function-extractor_v3_e94a9b0d_20260107_114239.html)

## Features

- **Declarative Configuration**: Define everything in YAML - no code required
- **Prompt Templates**: Define prompts with variables using Jinja2-style `{variable}` syntax
- **Test Cases**: Create comprehensive test suites with expected outputs
- **Multiple Metrics**:
  - `contains` - Verify required/forbidden substrings
  - `exact_match` - Check for exact string matching
  - `response_length` - Validate response length bounds
  - `regex_match` - Pattern matching with regular expressions
  - `llm_judge` - Use an LLM to score quality based on custom criteria
  - `composite` - Combine multiple metrics with weights
- **Comparison**: Compare multiple prompt variants side-by-side
- **Export Formats**: JSON, CSV, Markdown, and HTML reports
- **Simple CLI**: All operations via command-line interface

## Installation

```bash
cd prompt-eval-pipeline
pip install -e .
```

Set your Anthropic API key by creating a `.env` file:
```bash
cp .env.example .env
# Edit .env and add your API key
```

Your `.env` file should contain:
```
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

Get your API key at [console.anthropic.com/api-keys](https://console.anthropic.com/api-keys)

## Quick Start

### 1. Define your prompts and test cases

See the [Configuration Files](#configuration-files) section below for examples.

### 2. Run an evaluation

```bash
prompt-eval run configs/eval_narrative-function-extractor.yaml
```

### 3. View results

Results are saved to `results/` in multiple formats (JSON, CSV, Markdown, HTML).

## Configuration Files

### Prompt Definition (YAML)

Create individual prompt files in the `prompts/` directory:

#### Basic Prompt Format

```yaml
# prompts/qa_assistant.yaml
name: qa_assistant
description: A helpful Q&A assistant
version: "1.0"
system: You are a helpful assistant that provides accurate answers.
template: |
  Answer the following question in a {style} manner:

  {question}
```

### Complete Evaluation Configuration

Create a full evaluation config that includes everything. You can reference external prompt files or define prompts inline:

#### Option 1: Reference External Prompt Files (Recommended)

```yaml
# configs/eval_narrative-function-extractor.yaml
model: claude-opus-4-5-20251101
max_tokens: 4096
temperature: 0.1
evaluation_threshold: 0.5  # REQUIRED: Minimum score (0.0-1.0) for tests to pass

# Reference prompt variants from the prompts/ directory
prompts:
  - ../prompts/narrative-function-extractor/narrative-function-extractor_v3.yaml

# Test cases to run
test_cases:
  - name: cinderella_story
    inputs:
      text: "A young girl is mistreated by her stepmother and stepsisters. A fairy godmother helps her attend a ball where she meets the prince. She flees at midnight, leaving a glass slipper. The prince finds her using the slipper and they marry."
    expected_contains:
      - "Initial Situation"
      - "Villainy"
      - "Wedding"
    tags:
      - folktale

# Metrics to evaluate
metrics:
  - type: contains
    case_sensitive: false
  - type: response_length
    max_words: 500
```

## CLI Commands

### Run Evaluation from Config

```bash
# Run evaluation with all settings from config file
prompt-eval run configs/eval_narrative-function-extractor.yaml
```

**Options:**
- `-o, --output PATH` - Output directory (default: results/)
- `-f, --format [json|csv|markdown|html|all]` - Export format (default: all)
- `-m, --model TEXT` - Override model from config
- `-v, --verbose` - Verbose output
- `-q, --quiet` - Minimal output

## Evaluation Threshold

The `evaluation_threshold` parameter controls how strict your evaluations are. It sets the minimum score (from 0.0 to 1.0) that all metrics must achieve for a test to pass.

**This parameter is REQUIRED** - you must explicitly set it in each evaluation configuration file.

```yaml
# configs/eval_config.yaml
evaluation_threshold: 0.5  # Accepts partial matches (50%+)
evaluation_threshold: 1.0  # Requires perfect matches (100%)
evaluation_threshold: 0.8  # Requires 80%+ match
```

**How it works:**
- Each metric returns a score between 0.0 (complete failure) and 1.0 (perfect match)
- A test passes only if **ALL** metrics score >= `evaluation_threshold`
- For the `contains` metric: if you have 3 expected strings and only 2 match, the score is 0.667 (66.7%)
  - With `evaluation_threshold: 0.5` → test **passes** (0.667 >= 0.5)
  - With `evaluation_threshold: 1.0` → test **fails** (0.667 < 1.0)

**When to use strict thresholds (1.0):**
- Critical extractions where partial matches are wrong (e.g., extracting structured data)
- Validating exact formatting requirements
- Testing classification tasks where precision matters

**When to use lenient thresholds (0.5-0.7):**
- Testing overall response quality
- Validating that key concepts are present
- Allowing some flexibility in phrasing

## Metrics Reference

### Contains

Check for required or forbidden substrings:

```yaml
metrics:
  - type: contains
    case_sensitive: false  # Optional, default: true
```

Uses `expected_contains` and `expected_not_contains` from test cases.

### Exact Match

Check for exact string matching:

```yaml
metrics:
  - type: exact_match
    case_sensitive: true   # Optional, default: true
    strip_whitespace: true # Optional, default: true
```

Uses `expected` field from test cases.

### Response Length

Validate response length:

```yaml
metrics:
  - type: response_length
    min_chars: 10          # Optional
    max_chars: 500         # Optional
    min_words: 5           # Optional
    max_words: 100         # Optional
```

### Regex Match

Pattern matching with regular expressions:

```yaml
metrics:
  - type: regex_match
    pattern: "\\d{4}"      # Required: regex pattern
    must_match: true       # Optional, default: true
```

### LLM Judge

Use an LLM to score quality (requires additional API calls):

```yaml
metrics:
  - type: llm_judge
    criteria: |
      Evaluate the response on:
      1. Accuracy - Is the information correct?
      2. Clarity - Is it easy to understand?
      3. Completeness - Does it fully answer the question?
    model: claude-sonnet-4-20250514  # Optional, defaults to main model
    threshold: 0.7                    # Optional, default: 0.5
```

### Composite Metric

Combine multiple metrics with weights:

```yaml
metrics:
  - type: composite
    metrics:
      - type: contains
        weight: 0.5
      - type: response_length
        max_words: 100
        weight: 0.3
      - type: llm_judge
        criteria: "Is the response high quality?"
        weight: 0.2
```

## Output Formats

### JSON
Structured data with all evaluation details:
```json
{
  "run_id": "...",
  "prompt_name": "v1_simple",
  "model": "claude-sonnet-4-20250514",
  "results": [...]
}
```

### CSV
Tabular format for spreadsheet analysis:
```csv
test_case,passed,output,latency_ms
capital_france,true,"Paris",245
```

### Markdown
Human-readable report:
```markdown
# Evaluation Results: v1_simple
- Pass Rate: 100%
- Avg Latency: 245ms
```

### HTML
Formatted report with styling for easy viewing in browser.

## Project Structure

```
prompt-eval-pipeline/
├── src/prompt_eval/
│   ├── __init__.py      # Package initialization
│   ├── models.py        # Data models (internal)
│   ├── metrics.py       # Evaluation metrics (internal)
│   ├── evaluator.py     # Core evaluation engine (internal)
│   ├── loaders.py       # YAML/JSON file loaders (internal)
│   ├── exporters.py     # Result exporters (internal)
│   └── cli.py           # Command-line interface
├── prompts/             # Prompt template library (referenced by configs)
├── configs/             # Complete evaluation configurations (prompts + tests + metrics)
├── results/             # Generated reports (git-ignored)
└── pyproject.toml       # Project metadata and dependencies
```

## Tips and Best Practices

### Organizing Prompts

- Use descriptive names: `summarizer_v1_basic.yaml`, `summarizer_v2_structured.yaml`
- Add version numbers to track iterations
- Include descriptions explaining what makes each variant different
- Group related prompts in subdirectories if needed

### Writing Test Cases in Configs

- Define test cases inline in your evaluation configs
- Start with simple cases, then add edge cases
- Use tags to organize tests: `basic`, `edge_case`, `performance`, etc.
- Include both positive and negative expectations (`expected_contains`, `expected_not_contains`)
- Make test names descriptive: `handles_empty_input`, `respects_length_constraint`

### Choosing Metrics

- Start with simple metrics (`contains`, `response_length`)
- Add `llm_judge` for subjective quality assessment (but note it increases API costs)
- Use `composite` metrics to balance multiple concerns
- Set reasonable thresholds based on your requirements

### Running Evaluations

- Use `temperature: 0.0` for deterministic, reproducible results
- Run evaluations before and after prompt changes to measure impact
- Define multiple prompt variants in a single config to compare them
- Export to multiple formats for different audiences (JSON for processing, HTML for stakeholders)

## License

MIT
