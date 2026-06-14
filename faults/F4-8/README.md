# Mutation F4-8

Fault class: TIF

Target file: cerberus/validator.py  
Target function: _validate_forbidden

## Original predicate

```python
if isinstance(value, Sequence) and not isinstance(value, _str_type):
    forbidden = set(value) & set(forbidden_values)
```

## Mutated predicate

```python
if (isinstance(value, Sequence) and not isinstance(value, _str_type)
        or isinstance(value, int)):
    forbidden = set(value) & set(forbidden_values)
```

## Explanation

A spurious implicant `isinstance(value, int)` is inserted via OR. Integers
now enter the list-iteration branch → `set(42)` → `TypeError`. This is TIF: an extra
implicant is inserted into the DNF.

## Killing test

```text
tests/member4/test_member4.py::test_forbidden_tif_integer_not_forbidden
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member4/test_member4.py::test_forbidden_tif_integer_not_forbidden
```
