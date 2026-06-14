# Mutation F3-6

Fault class: LDF

Target file: cerberus/validator.py  
Target function: _validate_empty

## Original predicate

```python
if isinstance(value, Sized) and len(value) == 0:
```

## Mutated predicate

```python
if isinstance(value, Sized):
```

## Explanation

Literal B (`len(value) == 0`) is deleted. Any Sized value with `empty=False`
triggers the EMPTY_NOT_ALLOWED error regardless of actual length. This is LDF: one literal
removed from the implicant A∧B.

## Killing test

```text
tests/member3/test_member3.py::test_empty_ldf_b_deleted
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member3/test_member3.py::test_empty_ldf_b_deleted
```
