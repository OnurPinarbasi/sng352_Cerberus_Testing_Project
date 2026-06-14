# Mutation F1-6

Fault class: LDF

Target file: cerberus/validator.py  
Target function: _validate_minlength

## Original predicate

```python
if isinstance(value, Iterable) and len(value) < min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
```

## Mutated predicate

```python
if isinstance(value, Iterable):
    self._error(field, errors.MIN_LENGTH, len(value))
```

## Explanation

Literal B (`len(value) < min_length`) is deleted from the conjunction A∧B.
The surviving predicate is A alone (`isinstance(value, Iterable)`). Any iterable value,
regardless of its actual length, now triggers a MIN_LENGTH error. This is LDF: one literal
is removed from an implicant, weakening the gate without replacing it with anything.

## Killing test

```text
tests/member1/test_member1.py::test_minlength_ldf_b_deleted
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member1/test_member1.py::test_minlength_ldf_b_deleted
```
