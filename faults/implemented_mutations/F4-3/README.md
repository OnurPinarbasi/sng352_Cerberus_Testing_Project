# Mutation F4-3

Fault class: LNF

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
if isinstance(expected_values, Iterable) or isinstance(
    expected_values, _str_type
):
    expected_values = set((expected_values,))
else:
    expected_values = set(expected_values)
```

## Explanation

The literal `not isinstance(expected_values, Iterable)` (¬A) is negated to
`isinstance(expected_values, Iterable)` (A). The normalisation branch now fires when
`expected_values` IS iterable (e.g. a list), wrapping the list itself in a set rather
than expanding it. Membership checks become `{['a','b']} ⊆ value` instead of
`{'a','b'} ⊆ value`. This is LNF: one literal negation is removed.

## Killing test

```text
tests/member4/test_member4.py::test_contains_list_expected_all_present
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member4/test_member4.py::test_contains_list_expected_all_present
```
