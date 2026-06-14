# Mutation F1-8

Fault class: TNF

Target file: cerberus/validator.py  
Target function: _validate_minlength

## Original predicate

```python
if isinstance(value, Iterable) and len(value) < min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
```

## Mutated predicate

```python
if not isinstance(value, Iterable) or len(value) >= min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
```

## Explanation

The single implicant A∧B is negated to ¬(A∧B) = ¬A∨¬B. The error now
fires when the value is NOT iterable OR when its length already meets the minimum — the
exact complement of the original behaviour. This is TNF: the whole implicant is negated.

## Killing test

```text
tests/member1/test_member1.py::test_minlength_tnf_long_list
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member1/test_member1.py::test_minlength_tnf_long_list
```
