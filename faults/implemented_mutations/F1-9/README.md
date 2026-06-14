# Mutation F1-9

Fault class: TIF

Target file: cerberus/validator.py  
Target function: _validate_allowed

## Original predicate

```python
if isinstance(value, Iterable) and not isinstance(value, _str_type):
    unallowed = tuple(x for x in value if x not in allowed_values)
```

## Mutated predicate

```python
if (isinstance(value, Iterable) and not isinstance(value, _str_type)
        or isinstance(value, int)):
    unallowed = tuple(x for x in value if x not in allowed_values)
```

## Explanation

A spurious new implicant `isinstance(value, int)` is inserted into the
DNF via OR. Integers now enter the list-iteration branch even though the original logic
intended them to go through the scalar check. The iteration `for x in integer` raises
`TypeError`. This is TIF: an additional implicant is inserted into the disjunctive form.

## Killing test

```text
tests/member1/test_member1.py::test_allowed_tif_integer_in_allowed
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member1/test_member1.py::test_allowed_tif_integer_in_allowed
```
