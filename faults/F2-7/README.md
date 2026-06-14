# Mutation F2-7

Fault class: TNF

Target file: cerberus/validator.py  
Target function: _validate_maxlength

## Original predicate

```python
if isinstance(value, Iterable) and len(value) > max_length:
    self._error(field, errors.MAX_LENGTH, len(value))
```

## Mutated predicate

```python
if not isinstance(value, Iterable) or len(value) <= max_length:
    self._error(field, errors.MAX_LENGTH, len(value))
```

## Explanation

A∧B negated to ¬A∨¬B. The error now fires when the value is NOT iterable
OR when it is within the limit — the complete inverse of intended behaviour. This is TNF:
the single implicant is negated.

## Killing test

```text
tests/member2/test_member2.py::test_maxlength_tnf_within_limit
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member2/test_member2.py::test_maxlength_tnf_within_limit
```
