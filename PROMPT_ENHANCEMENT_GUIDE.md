# Prompt Enhancement Guide

This guide explains the enhanced prompt format with rules, skills, examples, and thinking process.

## Overview

The Prompt model now supports structured prompt engineering features to improve Claude's performance:

- **Rules**: Explicit constraints and guidelines
- **Skills**: Capabilities and techniques to apply
- **Examples**: Few-shot learning examples
- **Thinking Process**: Chain-of-thought guidance

## Enhanced YAML Format

```yaml
name: my_prompt
description: What this prompt does
version: "1.0"
system: Base system message

# NEW: Rules the model should follow
rules:
  - Rule 1
  - Rule 2
  - Rule 3

# NEW: Skills to apply
skills:
  - Skill 1
  - Skill 2

# NEW: Few-shot examples (optional)
examples:
  - input: "Example input 1"
    output: "Expected output 1"
  - input: "Example input 2"
    output: "Expected output 2"

# NEW: Chain-of-thought guidance (optional)
thinking_process: |
  Step-by-step reasoning guidance...

template: |
  Your main prompt template with {variables}
```

## How It Works

### System Prompt Construction

The system prompt is built from:
1. Base `system` message
2. `<rules>` section (if rules provided)
3. `<skills>` section (if skills provided)
4. `<thinking_process>` section (if provided)

Example output:
```
You are a philosopher specializing in logic.

<rules>
- Rule 1
- Rule 2
</rules>

<skills>
- Skill 1
- Skill 2
</skills>

<thinking_process>
Step-by-step guidance...
</thinking_process>
```

### User Prompt Construction

The user prompt includes:
1. `<examples>` section (if examples provided)
2. The rendered `template` with variables

Example output:
```
<examples>

Example 1:
input: Example input
output: Expected output

Example 2:
input: Another input
output: Another output
</examples>

[Your template rendered with variables]
```

## Best Practices

### Rules
- Be specific and actionable
- Focus on constraints and guidelines
- Keep rules concise and clear
- Use 3-7 rules (avoid overwhelming)

### Skills
- List relevant capabilities to activate
- Use domain-specific terminology
- Reference specific techniques or frameworks
- Keep to 3-5 key skills

### Examples
- Provide 2-5 diverse examples
- Cover edge cases
- Show clear input-output patterns
- Use realistic scenarios

### Thinking Process
- Provide step-by-step reasoning guidance
- Use numbered or bulleted steps
- Keep it concise (3-5 steps)
- Focus on the analysis approach

## Example: Definition Extractor

See [prompts/definition-extractor/definition-extractor_v4.yaml](prompts/definition-extractor/definition-extractor_v4.yaml) for a complete example.

## Backward Compatibility

All new fields are optional. Existing prompts without these fields will continue to work exactly as before:

```yaml
# This still works fine
name: simple_prompt
system: You are helpful
template: Answer this: {question}
```

## Migration Guide

To enhance an existing prompt:

1. **Add rules** - What constraints should the model follow?
2. **Add skills** - What techniques should it apply?
3. **Add examples** - What does good output look like?
4. **Add thinking_process** - How should it reason? (optional)

Start with rules and skills, then add examples if needed. The thinking_process is optional and best for complex reasoning tasks.
