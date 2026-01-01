"""Loaders for prompts and test cases from YAML/JSON files.

INTERNAL MODULE: Loaders are used internally by the CLI to parse YAML configuration files.
Users should create YAML files following the documented format - this module handles the parsing.
"""

import json
from pathlib import Path
from typing import Any

import yaml

from prompt_eval.models import Prompt, TestCase


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_file(path: str | Path) -> dict[str, Any]:
    """Load a YAML or JSON file based on extension."""
    path = Path(path)
    if path.suffix in (".yaml", ".yml"):
        return load_yaml(path)
    elif path.suffix == ".json":
        return load_json(path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


def load_prompt(path: str | Path) -> Prompt:
    """Load a single prompt from a YAML/JSON file (internal use only)."""
    path = Path(path)
    data = load_file(path)

    # Resolve pdf_path relative to the prompt file location
    if "pdf_path" in data and data["pdf_path"]:
        pdf_path = Path(data["pdf_path"])
        if not pdf_path.is_absolute():
            # Resolve relative to the prompt file's directory
            data["pdf_path"] = str(path.parent / pdf_path)

    return Prompt(**data)


def load_eval_config(path: str | Path) -> dict[str, Any]:
    """
    Load a complete evaluation configuration.

    Expected format:
    ```yaml
    model: claude-sonnet-4-20250514
    max_tokens: 1024
    temperature: 0.0
    evaluation_threshold: 0.5  # REQUIRED

    prompts:
      - prompts/summarizer_v1.yaml  # File path reference
      - prompts/summarizer_v2.yaml
    # OR inline definitions:
    #   - name: v1
    #     template: "..."

    test_cases:
      - name: test1
        inputs: {question: "..."}
        expected_contains: ["..."]

    metrics:
      - type: contains
      - type: llm_judge
        criteria: "..."
    ```
    """
    config_path = Path(path)
    data = load_file(config_path)

    config = {
        "model": data.get("model", "claude-sonnet-4-20250514"),
        "max_tokens": data.get("max_tokens", 1024),
        "temperature": data.get("temperature", 0.0),
        "evaluation_threshold": data["evaluation_threshold"],  # Required parameter
    }

    # Load prompts (support both file paths and inline definitions)
    if "prompts" in data:
        prompts = []
        for prompt_item in data["prompts"]:
            if isinstance(prompt_item, str):
                # It's a file path reference
                prompt_path = config_path.parent / prompt_item
                prompts.append(load_prompt(prompt_path))
            elif isinstance(prompt_item, dict):
                # It's an inline prompt definition
                prompts.append(Prompt(**prompt_item))
            else:
                raise ValueError(f"Invalid prompt format: {prompt_item}")
        config["prompts"] = prompts
    elif "prompt" in data:
        config["prompts"] = [Prompt(**data["prompt"])]

    # Load test cases
    if "test_cases" in data:
        config["test_cases"] = [TestCase(**tc) for tc in data["test_cases"]]
    elif "tests" in data:
        config["test_cases"] = [TestCase(**tc) for tc in data["tests"]]

    # Store raw metrics config for later instantiation
    config["metrics_config"] = data.get("metrics", [])

    return config
