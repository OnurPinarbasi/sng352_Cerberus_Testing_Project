# Mutation F1-7

Fault class: LRF

Target file: cerberus/validator.py  
Target function: _validate_minlength

## Original predicate

```python
if isinstance(value, Iterable) and len(value) < min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
```

## Mutated predicate

```python
if isinstance(value, Iterable) and len(value) <= min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
```

## Explanation

The strict-less-than operator `<` in literal B is replaced with `<=`. A
value whose length exactly equals `min_length` now incorrectly triggers a MIN_LENGTH
error, shifting the valid boundary by one. This is LRF: a comparison operator literal is
replaced with a semantically adjacent operator.

## Killing test

```text
tests/member1/test_member1.py::test_minlength_lrf_boundary
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member1/test_member1.py::test_minlength_lrf_boundary
```
