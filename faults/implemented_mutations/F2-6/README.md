# Mutation F2-6

Fault class: LDF

Target file: cerberus/validator.py  
Target function: _validate_maxlength

## Original predicate

```python
if isinstance(value, Iterable) and len(value) > max_length:
    self._error(field, errors.MAX_LENGTH, len(value))
```

## Mutated predicate

```python
if isinstance(value, Iterable):
    self._error(field, errors.MAX_LENGTH, len(value))
```

## Explanation

Literal B (`len(value) > max_length`) is deleted from the conjunction A∧B.
Any iterable value now triggers MAX_LENGTH, regardless of its actual length. This is LDF:
one literal removed from an implicant.

## Killing test

```text
tests/member2/test_member2.py::test_maxlength_ldf_b_deleted
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member2/test_member2.py::test_maxlength_ldf_b_deleted
```
