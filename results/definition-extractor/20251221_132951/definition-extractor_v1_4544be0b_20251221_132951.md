# Evaluation Report: definition-extractor_v1

**Run ID:** 4544be0b
**Model:** claude-sonnet-4-20250514
**Date:** 2025-12-21 13:28:54

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | 3 |
| Passed | 2 |
| Failed | 1 |
| Pass Rate | 66.7% |
| Avg Latency | 6473 ms |
| Total Tokens | 797 |

## Results

| Test Case | Passed | Latency (ms) | Metrics |
|-----------|--------|--------------|---------|
| proposition 2.201 | ✅ | 7115 | contains=1.00 |
| proposition 6.44 | ❌ | 7341 | contains=0.00 |
| proposition 3.5 | ✅ | 4961 | contains=1.00 |

## Failed Tests Details

### proposition 6.44

**Input:**
```
Please consider the following proposition:

Not how the world is, is the mystical, but that it is.

State if this proposition is a definition.

Your answer must follow this format:
Is a definition: yes|no
Word defined: the word|none

```

**Output:**
```
Looking at this proposition: "Not how the world is, is the mystical, but that it is."

This statement is making a substantive claim about the nature of the mystical - specifically that the mystical consists not in the particular way the world happens to be (its specific properties or states of affairs), but rather in the sheer fact of its existence. This is a philosophical thesis about what constitutes the mystical experience or dimension of reality.

While the statement does tell us something a...
```

**Metrics:** {'contains': 0.0}
