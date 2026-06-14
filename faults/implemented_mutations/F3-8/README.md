# Mutation F3-8

Fault class: TNF

Target file: cerberus/validator.py  
Target function: _validate_empty

## Original predicate

```python
if isinstance(value, Sized) and len(value) == 0:
```

## Mutated predicate

```python
if not isinstance(value, Sized) or len(value) != 0:
```

## Explanation

Implicant A∧B negated to ¬A∨¬B. The error fires for non-Sized values or
for non-empty containers — the exact inverse of the intended test for emptiness.
This is TNF: the implicant is negated in full.

## Killing test

```text
tests/member3/test_member3.py::test_empty_tnf_non_empty
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member3/test_member3.py::test_empty_tnf_non_empty
```
