# Mutation F1-11

Fault class: ORF*

Target file: cerberus/validator.py  
Target function: _validate_minlength

## Original predicate

```python
if isinstance(value, Iterable) and len(value) < min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
```

## Mutated predicate

```python
if isinstance(value, Iterable) or len(value) < min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
```

## Explanation

The conjunction A∧B is replaced by the disjunction A∨B. The error now
fires whenever the value is iterable (regardless of length) OR whenever the value is
shorter than the minimum (regardless of type). Any list, regardless of whether it is too
short, triggers an error. This is ORF\*: the AND operator is replaced by OR, weakening
the gate.

## Killing test

```text
tests/member1/test_member1.py::test_minlength_orf_star_long_list
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member1/test_member1.py::test_minlength_orf_star_long_list
```
