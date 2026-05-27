# Prompt Evaluation Pipeline

## Complete Documentation

**Version:** 0.1.0
**A declarative YAML-based framework for testing and comparing LLM prompts**

---

## Table of Contents

1. [Introduction](#1-introduction)
   - [What is Prompt Engineering?](#11-what-is-prompt-engineering)
   - [What is Prompt Evaluation?](#12-what-is-prompt-evaluation)
   - [Why Use This Framework?](#13-why-use-this-framework)
2. [Quick Start](#2-quick-start)
3. [Installation](#3-installation)
4. [Architecture Overview](#4-architecture-overview)
5. [CLI Reference](#5-cli-reference)
6. [Configuration Reference](#6-configuration-reference)
7. [Metrics Reference](#7-metrics-reference)
8. [Tutorial: Building a Q&A Chatbot Evaluation](#8-tutorial-building-a-qa-chatbot-evaluation)
9. [Sequence Diagrams](#9-sequence-diagrams)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Introduction

### 1.1 What is Prompt Engineering?

**Prompt engineering** is the practice of designing, refining, and optimizing the instructions (prompts) given to Large Language Models (LLMs) to achieve desired outputs. It involves:

- **Crafting clear instructions**: Writing precise directions that guide the model's behavior
- **Providing context**: Including relevant background information to improve response quality
- **Setting constraints**: Defining boundaries for format, length, tone, and content
- **Using examples**: Demonstrating expected input-output patterns (few-shot learning)
- **Iterative refinement**: Testing and improving prompts based on observed results

Prompt engineering is crucial because the same model can produce vastly different results depending on how instructions are framed. A well-engineered prompt can be the difference between a helpful, accurate response and a vague or incorrect one.

**Example of prompt engineering evolution:**

```
Version 1 (Basic):
"Answer the user's question."

Version 2 (With context):
"You are a helpful customer support assistant. Answer the user's question
clearly and concisely."

Version 3 (With constraints):
"You are a helpful customer support assistant for TechCorp. Answer the
user's question in 2-3 sentences. If you don't know the answer, say
'I'll need to check with our team.' Never make up information."
```

### 1.2 What is Prompt Evaluation?

**Prompt evaluation** is the systematic process of testing prompts against predefined criteria to measure their quality, consistency, and effectiveness. It answers the question: *"How well does this prompt perform?"*

Prompt evaluation involves:

- **Defining test cases**: Creating representative inputs with expected outcomes
- **Running evaluations**: Executing prompts against test cases and capturing outputs
- **Measuring quality**: Applying metrics to quantify how well outputs meet expectations
- **Comparing versions**: Testing multiple prompt variants to identify the best performer
- **Tracking regression**: Ensuring prompt changes don't degrade quality over time

**Why is prompt evaluation important?**

| Problem | Solution through Evaluation |
|---------|----------------------------|
| Inconsistent outputs | Measure consistency across multiple test cases |
| Quality degradation after changes | Run regression tests before deployment |
| Difficulty choosing between prompt versions | Compare metrics side-by-side |
| No objective quality measurement | Apply quantifiable metrics (accuracy, relevance) |
| Manual testing is time-consuming | Automate with declarative test configurations |

### 1.3 Why Use This Framework?

The **Prompt Evaluation Pipeline** provides:

- **Declarative configuration**: Define evaluations in YAML without writing code
- **Multiple metrics**: Built-in support for exact match, substring search, length validation, regex patterns, and LLM-based judging
- **Batch evaluation**: Run multiple test cases automatically
- **Prompt comparison**: Evaluate multiple prompt versions side-by-side
- **Multiple export formats**: Generate reports in JSON, CSV, Markdown, and HTML
- **Prompt caching**: Optimize API costs with Anthropic's prompt caching feature
- **Extensible design**: Easy to add custom metrics and exporters

---

## 2. Quick Start

Get started in 5 minutes:

**Step 1: Install the package**
```bash
pip install -e .
```

**Step 2: Set your API key**
```bash
export ANTHROPIC_API_KEY=your_key_here
```

**Step 3: Create a prompt file** (`prompts/qa_assistant.yaml`)
```yaml
name: qa_assistant_v1
version: "1.0"
description: "A helpful Q&A assistant"
system: |
  You are a helpful Q&A assistant. Answer questions accurately and concisely.
  If you don't know the answer, say "I don't know."
template: |
  Question: {question}
```

**Step 4: Create an evaluation config** (`configs/eval_qa.yaml`)
```yaml
model: claude-sonnet-4-20250514
max_tokens: 256
temperature: 0.0
evaluation_threshold: 0.8

prompts:
  - prompts/qa_assistant.yaml

test_cases:
  - name: capital_france
    inputs:
      question: "What is the capital of France?"
    expected_contains:
      - "Paris"

  - name: unknown_question
    inputs:
      question: "What color is the invisible dragon?"
    expected_contains:
      - "don't know"

metrics:
  - type: contains
    case_sensitive: false
```

**Step 5: Run the evaluation**
```bash
prompt-eval run configs/eval_qa.yaml
```

**Step 6: View results**
Results are saved in `results/qa/<timestamp>/` with JSON, CSV, Markdown, and HTML reports.

---

## 3. Installation

### 3.1 Requirements

- Python 3.10 or higher
- An Anthropic API key

### 3.2 Installation Steps

**Option A: Install from source (recommended for development)**

```bash
# Clone the repository
git clone https://github.com/your-org/prompt-eval-pipeline.git
cd prompt-eval-pipeline

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# Install development dependencies (optional)
pip install -e ".[dev]"
```

**Option B: Install dependencies manually**

```bash
pip install anthropic>=0.40.0 pydantic>=2.0.0 pyyaml>=6.0 rich>=13.0.0 pandas>=2.0.0 jinja2>=3.0.0 click>=8.0.0 python-dotenv>=1.0.0 pypdf>=5.0.0
```

### 3.3 Configuration

**Setting the API Key**

Option 1: Environment variable
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Option 2: Create a `.env` file in the project root
```
ANTHROPIC_API_KEY=sk-ant-...
```

**Verify installation**
```bash
prompt-eval --version
# Output: prompt-eval, version 0.1.0
```

---

## 4. Architecture Overview

The framework follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI Layer                               │
│                      (cli.py - Click)                           │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                    Configuration Layer                          │
│                 (loaders.py - YAML/JSON)                        │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                    Evaluation Engine                            │
│                (evaluator.py - Anthropic API)                   │
└───────────┬─────────────────────────────────┬───────────────────┘
            │                                 │
┌───────────▼───────────┐       ┌─────────────▼─────────────────┐
│     Metrics Layer     │       │       Export Layer            │
│     (metrics.py)      │       │     (exporters.py)            │
│ - Contains            │       │ - JSON                        │
│ - ExactMatch          │       │ - CSV                         │
│ - ResponseLength      │       │ - Markdown                    │
│ - RegexMatch          │       │ - HTML                        │
│ - LLMJudge            │       └───────────────────────────────┘
│ - Composite           │
└───────────────────────┘
```

**Component Responsibilities:**

| Component | File | Responsibility |
|-----------|------|----------------|
| CLI | `cli.py` | Command-line interface, orchestration |
| Loaders | `loaders.py` | Parse YAML/JSON configurations |
| Models | `models.py` | Data structures (Prompt, TestCase, EvalResult) |
| Evaluator | `evaluator.py` | Execute prompts, call Anthropic API |
| Metrics | `metrics.py` | Score outputs against expectations |
| Exporters | `exporters.py` | Generate reports in multiple formats |

---

## 5. CLI Reference

### 5.1 Main Command

```bash
prompt-eval [OPTIONS] COMMAND [ARGS]
```

**Global Options:**
- `--version`: Show version and exit
- `--help`: Show help message and exit

### 5.2 Run Command

Execute an evaluation from a configuration file.

```bash
prompt-eval run [OPTIONS] CONFIG_FILE
```

**Arguments:**
- `CONFIG_FILE`: Path to the evaluation configuration file (YAML or JSON)

**Options:**

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output directory for results | `results/<name>/<timestamp>` |
| `--format` | `-f` | Output format: `json`, `csv`, `markdown`, `html`, `all` | `all` |
| `--model` | `-m` | Override model from config | Config value |
| `--verbose` | `-v` | Enable verbose output | `True` |
| `--quiet` | `-q` | Disable verbose output | `False` |

**Examples:**

```bash
# Basic run
prompt-eval run configs/eval_qa.yaml

# Specify output directory
prompt-eval run configs/eval_qa.yaml -o results/experiment1

# Only generate JSON output
prompt-eval run configs/eval_qa.yaml -f json

# Override model
prompt-eval run configs/eval_qa.yaml -m claude-opus-4-5-20251101

# Quiet mode (minimal output)
prompt-eval run configs/eval_qa.yaml -q
```

---

## 6. Configuration Reference

### 6.1 Evaluation Configuration

The main configuration file defines the evaluation parameters.

**File:** `configs/eval_<name>.yaml`

```yaml
# Model Configuration
model: claude-sonnet-4-20250514    # Required: Anthropic model ID
max_tokens: 1024                    # Optional: Max response tokens (default: 1024)
temperature: 0.0                    # Optional: Sampling temperature (default: 0.0)
evaluation_threshold: 0.8           # Required: Pass/fail threshold (0.0-1.0)

# Prompts to evaluate (file references or inline)
prompts:
  - prompts/assistant_v1.yaml       # File reference
  - prompts/assistant_v2.yaml       # Multiple prompts for comparison

# Test cases
test_cases:
  - name: test_1
    inputs:
      question: "What is 2+2?"
    expected_contains:
      - "4"
    expected_not_contains:
      - "5"
    tags:
      - math
      - basic

# Metrics configuration
metrics:
  - type: contains
    case_sensitive: false
  - type: response_length
    min_words: 10
    max_words: 100
```

### 6.2 Prompt Configuration

Prompts define the instructions sent to the LLM.

**File:** `prompts/<name>.yaml`

```yaml
# Basic Information
name: qa_assistant_v1              # Required: Unique identifier
version: "1.0"                      # Optional: Version string
description: "Q&A assistant"        # Optional: Description

# Prompt Content
system: |                           # Optional: System prompt
  You are a helpful assistant.

template: |                         # Required: User prompt template
  Question: {question}
  Please provide a clear answer.

# Advanced Prompt Engineering
rules:                              # Optional: Behavioral rules
  - Always be polite
  - Never make up information
  - Cite sources when possible

skills:                             # Optional: Skills/capabilities
  - Answering factual questions
  - Explaining complex topics simply

thinking_process: |                 # Optional: Chain-of-thought guidance
  1. Understand the question
  2. Recall relevant information
  3. Formulate a clear answer

examples:                           # Optional: Few-shot examples
  - input: "What is the sun?"
    output: "The sun is a star at the center of our solar system."

# File Caching (for large reference documents)
cached_files:                       # Optional: Files to cache
  - reference/knowledge_base.md
  - reference/faq.txt
```

### 6.3 Test Case Configuration

Test cases define inputs and expected outputs.

```yaml
test_cases:
  - name: unique_test_name          # Required: Unique identifier
    inputs:                          # Required: Template variables
      question: "What is Python?"
      context: "Programming languages"
    expected: "Python is a programming language"  # Optional: Exact match
    expected_contains:               # Optional: Required substrings
      - "programming"
      - "language"
    expected_not_contains:           # Optional: Forbidden substrings
      - "snake"
      - "reptile"
    tags:                            # Optional: Tags for filtering
      - programming
      - easy
    metadata:                        # Optional: Additional data
      difficulty: easy
      category: tech
```

### 6.4 Configuration Parameters Summary

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `model` | Yes | string | Anthropic model ID |
| `max_tokens` | No | int | Maximum response tokens (default: 1024) |
| `temperature` | No | float | Sampling temperature 0.0-1.0 (default: 0.0) |
| `evaluation_threshold` | Yes | float | Pass/fail threshold 0.0-1.0 |
| `prompts` | Yes | list | Prompt file paths or inline definitions |
| `test_cases` | Yes | list | Test case definitions |
| `metrics` | No | list | Metric configurations (default: contains) |

---

## 7. Metrics Reference

Metrics measure how well the LLM output matches expectations.

### 7.1 Contains Metric

Checks if the output contains required substrings and excludes forbidden ones.

```yaml
metrics:
  - type: contains
    case_sensitive: false    # Optional: Case-sensitive matching (default: false)
```

**Scoring:**
- Score = (matched required strings / total required strings) × (1 - violations / total forbidden strings)
- Range: 0.0 to 1.0

**Example:**
```yaml
test_cases:
  - name: greeting
    inputs:
      message: "Hello"
    expected_contains:
      - "hello"
      - "hi"
    expected_not_contains:
      - "goodbye"
```

### 7.2 Exact Match Metric

Checks if the output exactly matches the expected value.

```yaml
metrics:
  - type: exact_match
    case_sensitive: false    # Optional: Case-sensitive (default: false)
    strip: true              # Optional: Strip whitespace (default: true)
```

**Scoring:**
- Score = 1.0 if exact match, 0.0 otherwise

**Example:**
```yaml
test_cases:
  - name: math
    inputs:
      equation: "2+2"
    expected: "4"
```

### 7.3 Response Length Metric

Validates the response length in characters or words.

```yaml
metrics:
  - type: response_length
    min_chars: 100           # Optional: Minimum characters
    max_chars: 500           # Optional: Maximum characters
    min_words: 20            # Optional: Minimum words
    max_words: 100           # Optional: Maximum words
```

**Scoring:**
- Score = 1.0 if within bounds, 0.0 otherwise

### 7.4 Regex Match Metric

Checks if the output matches a regular expression pattern.

```yaml
metrics:
  - type: regex_match
    pattern: "\\d{4}-\\d{2}-\\d{2}"    # Date pattern YYYY-MM-DD
```

**Scoring:**
- Score = 1.0 if pattern found, 0.0 otherwise

### 7.5 LLM Judge Metric

Uses another LLM to evaluate the quality of the output.

```yaml
metrics:
  - type: llm_judge
    criteria: |
      Evaluate if the response is:
      1. Accurate and factual
      2. Clear and well-organized
      3. Appropriately detailed
    model: claude-sonnet-4-20250514    # Optional: Judge model
```

**Scoring:**
- Score = 0.0 to 1.0 as determined by the judge LLM

### 7.6 Composite Metric

Combines multiple metrics with weights.

```yaml
metrics:
  - type: composite
    metrics:
      - type: contains
        weight: 0.5
      - type: response_length
        min_words: 50
        weight: 0.3
      - type: llm_judge
        criteria: "Is the response helpful?"
        weight: 0.2
```

### 7.7 Metrics Summary Table

| Metric | Use Case | Scoring |
|--------|----------|---------|
| `contains` | Check for required/forbidden content | Ratio of matches |
| `exact_match` | Precise output matching | Binary (0 or 1) |
| `response_length` | Enforce length constraints | Binary (0 or 1) |
| `regex_match` | Pattern validation | Binary (0 or 1) |
| `llm_judge` | Subjective quality assessment | Continuous (0-1) |
| `composite` | Combined evaluation | Weighted average |

---

## 8. Tutorial: Building a Q&A Chatbot Evaluation

This tutorial walks through creating a complete evaluation pipeline for a Q&A chatbot assistant.

### 8.1 Scenario

You're building a general-purpose Q&A chatbot that should:
- Answer factual questions accurately
- Admit when it doesn't know something
- Provide concise but complete answers
- Avoid making up information

### 8.2 Step 1: Create the Project Structure

```
my-qa-chatbot/
├── prompts/
│   ├── qa_v1.yaml
│   └── qa_v2.yaml
├── configs/
│   └── eval_qa.yaml
└── results/
```

### 8.3 Step 2: Define Prompt Version 1

**File:** `prompts/qa_v1.yaml`

```yaml
name: qa_chatbot_v1
version: "1.0"
description: "Basic Q&A chatbot - first iteration"

system: |
  You are a helpful Q&A assistant. Answer user questions accurately.

template: |
  User Question: {question}
```

### 8.4 Step 3: Define Prompt Version 2 (Improved)

**File:** `prompts/qa_v2.yaml`

```yaml
name: qa_chatbot_v2
version: "2.0"
description: "Improved Q&A chatbot with better instructions"

system: |
  You are a knowledgeable and helpful Q&A assistant.

rules:
  - Provide accurate, factual information
  - Keep answers concise (2-4 sentences for simple questions)
  - If you don't know the answer, say "I don't have information about that"
  - Never make up facts or statistics
  - Use simple language that anyone can understand

skills:
  - Answering general knowledge questions
  - Explaining concepts clearly
  - Acknowledging limitations honestly

thinking_process: |
  1. Understand what the user is asking
  2. Determine if I have reliable information to answer
  3. If yes, formulate a clear and concise response
  4. If no, honestly state that I don't know

template: |
  Please answer the following question:

  {question}
```

### 8.5 Step 4: Create Test Cases

**File:** `configs/eval_qa.yaml`

```yaml
model: claude-sonnet-4-20250514
max_tokens: 512
temperature: 0.0
evaluation_threshold: 0.8

prompts:
  - prompts/qa_v1.yaml
  - prompts/qa_v2.yaml

test_cases:
  # Factual questions - should answer correctly
  - name: capital_france
    inputs:
      question: "What is the capital of France?"
    expected_contains:
      - "Paris"
    tags:
      - geography
      - factual

  - name: water_formula
    inputs:
      question: "What is the chemical formula for water?"
    expected_contains:
      - "H2O"
    tags:
      - science
      - factual

  - name: shakespeare_author
    inputs:
      question: "Who wrote Romeo and Juliet?"
    expected_contains:
      - "Shakespeare"
    tags:
      - literature
      - factual

  # Unknown questions - should admit ignorance
  - name: unknown_personal
    inputs:
      question: "What did I have for breakfast yesterday?"
    expected_contains:
      - "don't"
    expected_not_contains:
      - "you had"
      - "you ate"
    tags:
      - unknown
      - boundary

  - name: future_prediction
    inputs:
      question: "What will the stock market do tomorrow?"
    expected_contains:
      - "cannot"
    expected_not_contains:
      - "will rise"
      - "will fall"
    tags:
      - unknown
      - boundary

  # Edge cases
  - name: ambiguous_question
    inputs:
      question: "What is the best?"
    expected_not_contains:
      - "definitely"
      - "obviously"
    tags:
      - edge_case

metrics:
  - type: contains
    case_sensitive: false
  - type: response_length
    min_words: 5
    max_words: 200
```

### 8.6 Step 5: Run the Evaluation

```bash
# Run evaluation comparing both prompt versions
prompt-eval run configs/eval_qa.yaml

# Output:
# Loading config from configs/eval_qa.yaml...
#
# Starting evaluation run: abc12345
# Prompt: qa_chatbot_v1 | Model: claude-sonnet-4-20250514 | Tests: 6
# Evaluating... ━━━━━━━━━━━━━━━━━━━━━━ 100%
#
# ┌──────────────────────────────────┐
# │   Evaluation Summary: abc12345   │
# ├────────────┬─────────────────────┤
# │ Metric     │ Value               │
# ├────────────┼─────────────────────┤
# │ Prompt     │ qa_chatbot_v1       │
# │ Pass Rate  │ 66.7%               │
# │ Passed     │ 4                   │
# │ Failed     │ 2                   │
# └────────────┴─────────────────────┘
#
# Starting evaluation run: def67890
# Prompt: qa_chatbot_v2 | Model: claude-sonnet-4-20250514 | Tests: 6
# Evaluating... ━━━━━━━━━━━━━━━━━━━━━━ 100%
#
# ┌──────────────────────────────────┐
# │   Evaluation Summary: def67890   │
# ├────────────┬─────────────────────┤
# │ Metric     │ Value               │
# ├────────────┼─────────────────────┤
# │ Prompt     │ qa_chatbot_v2       │
# │ Pass Rate  │ 100.0%              │
# │ Passed     │ 6                   │
# │ Failed     │ 0                   │
# └────────────┴─────────────────────┘
```

### 8.7 Step 6: Analyze Results

Check the generated reports in `results/qa/<timestamp>/`:

- **comparison.md**: Side-by-side comparison of prompt versions
- **qa_chatbot_v1_*.html**: Detailed HTML report for version 1
- **qa_chatbot_v2_*.html**: Detailed HTML report for version 2

### 8.8 Step 7: Iterate and Improve

Based on the results:
1. Identify failing test cases
2. Analyze why the prompt failed
3. Modify the prompt to address issues
4. Re-run the evaluation
5. Repeat until satisfied

---

## 9. Sequence Diagrams

### 9.1 Single Prompt Evaluation Flow

```
┌─────┐          ┌─────┐          ┌────────┐          ┌─────────┐          ┌─────────┐
│User │          │ CLI │          │Loader  │          │Evaluator│          │Anthropic│
└──┬──┘          └──┬──┘          └───┬────┘          └────┬────┘          └────┬────┘
   │                │                 │                    │                    │
   │ prompt-eval    │                 │                    │                    │
   │ run config.yaml│                 │                    │                    │
   │───────────────>│                 │                    │                    │
   │                │                 │                    │                    │
   │                │ load_eval_config│                    │                    │
   │                │────────────────>│                    │                    │
   │                │                 │                    │                    │
   │                │     config      │                    │                    │
   │                │<────────────────│                    │                    │
   │                │                 │                    │                    │
   │                │     evaluate(prompt, test_cases)     │                    │
   │                │─────────────────────────────────────>│                    │
   │                │                 │                    │                    │
   │                │                 │                    │  ┌────────────────┐│
   │                │                 │                    │  │ For each       ││
   │                │                 │                    │  │ test case      ││
   │                │                 │                    │  └───────┬────────┘│
   │                │                 │                    │          │         │
   │                │                 │                    │ messages.create    │
   │                │                 │                    │─────────────────────>
   │                │                 │                    │          │         │
   │                │                 │                    │     response       │
   │                │                 │                    │<─────────────────────
   │                │                 │                    │          │         │
   │                │                 │                    │ calculate metrics  │
   │                │                 │                    │──────────┤         │
   │                │                 │                    │          │         │
   │                │                 │                    │  ┌───────┴────────┐│
   │                │                 │                    │  │ End loop       ││
   │                │                 │                    │  └────────────────┘│
   │                │                 │                    │                    │
   │                │      EvalRun (results)               │                    │
   │                │<─────────────────────────────────────│                    │
   │                │                 │                    │                    │
   │                │ export results  │                    │                    │
   │                │────────────────>│                    │                    │
   │                │                 │                    │                    │
   │  Results saved │                 │                    │                    │
   │<───────────────│                 │                    │                    │
   │                │                 │                    │                    │
```

### 9.2 Multi-Prompt Comparison Flow

```
┌─────┐          ┌─────┐          ┌─────────┐          ┌────────┐
│User │          │ CLI │          │Evaluator│          │Exporter│
└──┬──┘          └──┬──┘          └────┬────┘          └───┬────┘
   │                │                  │                   │
   │ run config     │                  │                   │
   │ (2 prompts)    │                  │                   │
   │───────────────>│                  │                   │
   │                │                  │                   │
   │                │  ┌──────────────────────────────┐    │
   │                │  │ For each prompt              │    │
   │                │  └───────────────┬──────────────┘    │
   │                │                  │                   │
   │                │ evaluate(prompt1)│                   │
   │                │─────────────────>│                   │
   │                │                  │                   │
   │                │     EvalRun 1    │                   │
   │                │<─────────────────│                   │
   │                │                  │                   │
   │                │ evaluate(prompt2)│                   │
   │                │─────────────────>│                   │
   │                │                  │                   │
   │                │     EvalRun 2    │                   │
   │                │<─────────────────│                   │
   │                │  └───────────────┴──────────────┘    │
   │                │                  │                   │
   │                │ export_all(run1) │                   │
   │                │─────────────────────────────────────>│
   │                │                  │                   │
   │                │ export_all(run2) │                   │
   │                │─────────────────────────────────────>│
   │                │                  │                   │
   │                │ compare_runs([run1, run2])           │
   │                │─────────────────────────────────────>│
   │                │                  │                   │
   │                │        comparison.md                 │
   │                │<─────────────────────────────────────│
   │                │                  │                   │
   │ Results +      │                  │                   │
   │ comparison     │                  │                   │
   │<───────────────│                  │                   │
   │                │                  │                   │
```

### 9.3 Metrics Calculation Flow

```
┌─────────┐          ┌───────────┐          ┌────────┐          ┌──────────┐
│Evaluator│          │ Contains  │          │LLMJudge│          │Anthropic │
└────┬────┘          └─────┬─────┘          └───┬────┘          └─────┬────┘
     │                     │                    │                     │
     │ score(output,       │                    │                     │
     │       test_case)    │                    │                     │
     │────────────────────>│                    │                     │
     │                     │                    │                     │
     │                     │ Check expected_    │                     │
     │                     │ contains           │                     │
     │                     │──────────┐         │                     │
     │                     │          │         │                     │
     │                     │<─────────┘         │                     │
     │                     │                    │                     │
     │                     │ Check expected_    │                     │
     │                     │ not_contains       │                     │
     │                     │──────────┐         │                     │
     │                     │          │         │                     │
     │                     │<─────────┘         │                     │
     │                     │                    │                     │
     │   contains_score    │                    │                     │
     │<────────────────────│                    │                     │
     │                     │                    │                     │
     │ score(output, test_case)                 │                     │
     │─────────────────────────────────────────>│                     │
     │                     │                    │                     │
     │                     │                    │ Build judge prompt  │
     │                     │                    │──────────┐          │
     │                     │                    │          │          │
     │                     │                    │<─────────┘          │
     │                     │                    │                     │
     │                     │                    │ messages.create     │
     │                     │                    │────────────────────>│
     │                     │                    │                     │
     │                     │                    │    score (0.0-1.0)  │
     │                     │                    │<────────────────────│
     │                     │                    │                     │
     │            llm_judge_score               │                     │
     │<────────────────────────────────────────│                     │
     │                     │                    │                     │
     │ Aggregate scores    │                    │                     │
     │ (all >= threshold?) │                    │                     │
     │──────────┐          │                    │                     │
     │          │          │                    │                     │
     │<─────────┘          │                    │                     │
     │                     │                    │                     │
     │ passed = True/False │                    │                     │
     │                     │                    │                     │
```

---

## 10. Troubleshooting

### 10.1 Common Errors

#### Error: "ANTHROPIC_API_KEY not set"

**Problem:** The API key is not configured.

**Solution:**
```bash
# Option 1: Set environment variable
export ANTHROPIC_API_KEY=sk-ant-...

# Option 2: Create .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

#### Error: "No prompts found in config"

**Problem:** The configuration file doesn't specify any prompts.

**Solution:** Add a `prompts` section to your config:
```yaml
prompts:
  - prompts/my_prompt.yaml
```

#### Error: "No test cases found in config"

**Problem:** The configuration file doesn't have test cases.

**Solution:** Add a `test_cases` section:
```yaml
test_cases:
  - name: test_1
    inputs:
      question: "Hello?"
    expected_contains:
      - "hello"
```

#### Error: "evaluation_threshold is required"

**Problem:** Missing required threshold parameter.

**Solution:** Add the threshold to your config:
```yaml
evaluation_threshold: 0.8
```

#### Error: "File not found: prompts/xyz.yaml"

**Problem:** The prompt file path is incorrect.

**Solution:**
- Check the file exists at the specified path
- Paths are relative to the config file location
- Use forward slashes even on Windows

### 10.2 Performance Issues

#### Slow Evaluation Speed

**Causes and solutions:**

1. **Large number of test cases**: Run in batches or use a faster model
2. **High max_tokens**: Reduce `max_tokens` if responses are shorter
3. **No prompt caching**: Use `cached_files` for large reference documents

#### High API Costs

**Solutions:**

1. Use prompt caching for repeated content:
   ```yaml
   cached_files:
     - reference/knowledge_base.md
   ```

2. Use a cheaper model for development:
   ```bash
   prompt-eval run config.yaml -m claude-haiku-3
   ```

3. Reduce test cases during development

### 10.3 Unexpected Results

#### Test Failing When It Should Pass

**Debugging steps:**

1. Check the HTML report for actual output
2. Verify `expected_contains` strings match exactly (case sensitivity)
3. Check for typos in expected values
4. Review the `evaluation_threshold` setting

#### All Tests Passing When Some Should Fail

**Debugging steps:**

1. Check if `expected_contains` is empty (defaults to pass)
2. Verify metrics are configured correctly
3. Lower the `evaluation_threshold` to be more strict

### 10.4 Configuration Debugging

**Validate your configuration:**

```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('configs/eval_qa.yaml'))"

# Run with verbose output
prompt-eval run configs/eval_qa.yaml -v
```

**Common YAML mistakes:**

```yaml
# Wrong: Missing quotes around special characters
expected_contains:
  - What's the answer?    # Error: apostrophe

# Correct: Quote strings with special characters
expected_contains:
  - "What's the answer?"

# Wrong: Incorrect indentation
test_cases:
- name: test1            # Error: missing indent
  inputs:
    q: "Hi"

# Correct: Proper indentation
test_cases:
  - name: test1
    inputs:
      q: "Hi"
```

### 10.5 Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/your-org/prompt-eval-pipeline/issues)
2. Review the source code documentation
3. Open a new issue with:
   - Your configuration file (redacted)
   - The error message
   - Steps to reproduce

---

## Appendix

### A. Supported Models

| Model ID | Description |
|----------|-------------|
| `claude-opus-4-5-20251101` | Most capable, best for complex tasks |
| `claude-sonnet-4-20250514` | Balanced performance and cost |
| `claude-haiku-3` | Fastest, best for simple tasks |

### B. File Format Support

| Format | Extension | Use Case |
|--------|-----------|----------|
| YAML | `.yaml`, `.yml` | Configuration files |
| JSON | `.json` | Configuration files |
| Markdown | `.md` | Reference documents |
| Text | `.txt` | Reference documents |
| PDF | `.pdf` | Reference documents |

### C. Output Formats

| Format | Extension | Best For |
|--------|-----------|----------|
| JSON | `.json` | Programmatic processing |
| CSV | `.csv` | Spreadsheet analysis |
| Markdown | `.md` | Documentation |
| HTML | `.html` | Visual review |

---

*Generated for Prompt Evaluation Pipeline v0.1.0*
