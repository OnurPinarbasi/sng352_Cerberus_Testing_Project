# Mutation F4-5

Fault class: LRF

Target file: cerberus/validator.py  
Target function: _validate_items

## Original predicate

```python
if len(items) != len(values):
    self._error(field, errors.ITEMS_LENGTH, len(items), len(values))
```

## Mutated predicate

```python
if len(items) == len(values):
    self._error(field, errors.ITEMS_LENGTH, len(items), len(values))
```

## Explanation

The relational operator `!=` is replaced with `==`. The length mismatch
error now fires when lengths are EQUAL and is suppressed when they DIFFER — the exact
opposite of the intended behaviour. This is LRF: a relational operator literal is replaced
with a semantically opposite operator.

## Killing test

```text
tests/member4/test_member4.py::test_items_length_mismatch
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member4/test_member4.py::test_items_length_mismatch
```
