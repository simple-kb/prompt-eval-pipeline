# Evaluation Report: definition-extractor_v2

**Run ID:** 8e000ab2
**Model:** claude-sonnet-4-20250514
**Date:** 2025-12-21 13:50:28

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | 3 |
| Passed | 2 |
| Failed | 1 |
| Pass Rate | 66.7% |
| Avg Latency | 6463 ms |
| Total Tokens | 797 |

## Results

| Test Case | Passed | Latency (ms) | Metrics |
|-----------|--------|--------------|---------|
| proposition 2.201 | ✅ | 6604 | contains=1.00 |
| proposition 6.44 | ❌ | 7625 | contains=0.00 |
| proposition 3.5 | ✅ | 5160 | contains=1.00 |

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

While the statement does tell us something about what "the mystical" refers to, it's not functioning as a definition in the strict sense. Rather, it's making a claim about where we should locate the mystical - in existence itself rather than in any particular features of what exists. A definition would typically take the form "The mystical is..." or "By 'mystical' we mean..." and would aim to give necessary and sufficient conditions for the term's application.

This appears to be a substantive philosophical claim (reminiscent of Wittgenstein's Tractus 6.44) rather than a definitional stipulation.

Is a definition: no
Word defined: none
```

**Metrics:** {'contains': 0.0}
