# Mutation F2-11

Fault class: ENF

Target file: cerberus/validator.py  
Target function: _validate_maxlength

## Original predicate

```python
if isinstance(value, Iterable) and len(value) > max_length:
    self._error(field, errors.MAX_LENGTH, len(value))
```

## Mutated predicate

```python
if not (isinstance(value, Iterable) and len(value) > max_length):
    self._error(field, errors.MAX_LENGTH, len(value))
```

## Explanation

The complete predicate is negated. The error now fires for values that are
within the limit (the common valid case) and is suppressed for values that exceed the
limit (the error case). This is ENF: the entire governing expression is negated.

## Killing test

```text
tests/member2/test_member2.py::test_maxlength_enf_within_limit
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member2/test_member2.py::test_maxlength_enf_within_limit
```
