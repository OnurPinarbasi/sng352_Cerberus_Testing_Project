# Mutation F4-9

Fault class: ORF+

Target file: cerberus/validator.py  
Target function: _validate_contains

## Original predicate

```python
if not isinstance(expected_values, Iterable) or isinstance(
    expected_values, _str_type
):
    expected_values = set((expected_values,))
else:
    expected_values = set(expected_values)
```

## Mutated predicate

```python
if not isinstance(expected_values, Iterable) and isinstance(
    expected_values, _str_type
):
    expected_values = set((expected_values,))
else:
    expected_values = set(expected_values)
```

## Explanation

¬A∨B replaced by ¬A∧B. Since `str` IS Iterable, `¬A=False` for strings →
`¬A∧B` is always False. Strings fall to the else branch → `set('abc')` = `{'a','b','c'}`
(characters) instead of `{'abc'}` (the string as one element). This is ORF+: OR replaced
with AND, killing the normalisation for string inputs.

## Killing test

```text
tests/member4/test_member4.py::test_contains_orf_plus_string_multi
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member4/test_member4.py::test_contains_orf_plus_string_multi
```
