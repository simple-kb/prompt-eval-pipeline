"""Prompt Evaluation Pipeline - Test and compare LLM prompts systematically.

This package provides a YAML-based declarative approach to evaluating and comparing
LLM prompts. Use the CLI command to run evaluations:

    prompt-eval run configs/eval_config.yaml

All classes and functions are internal implementation details.
External interaction should be through the CLI or YAML configuration files.
"""

from pathlib import Path
from dotenv import load_dotenv

# Load .env file from current directory or project root
load_dotenv()
# Also try loading from the package's parent directories
for parent in Path(__file__).resolve().parents:
    env_file = parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        break

__version__ = "0.1.0"

# No public API - use CLI commands instead
__all__ = []
