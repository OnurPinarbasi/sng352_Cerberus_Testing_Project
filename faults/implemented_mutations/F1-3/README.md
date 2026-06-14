# Mutation F1-3

Fault class: TOF

Target file: cerberus/validator.py  
Target function: _validate_allowed

## Original predicate

```python
if isinstance(value, Iterable) and not isinstance(value, _str_type):
    unallowed = tuple(x for x in value if x not in allowed_values)
    if unallowed:
        self._error(field, errors.UNALLOWED_VALUES, unallowed)
else:
    if value not in allowed_values:
        self._error(field, errors.UNALLOWED_VALUE, value)
```

## Mutated predicate

```python
if isinstance(value, Iterable):
    unallowed = tuple(x for x in value if x not in allowed_values)
    if unallowed:
        self._error(field, errors.UNALLOWED_VALUES, unallowed)
else:
    if value not in allowed_values:
        self._error(field, errors.UNALLOWED_VALUE, value)
```

## Explanation

The implicant `A ∧ ¬B` (isinstance Iterable AND NOT isinstance str) loses
the `¬B` literal — the guard that diverts strings to the scalar path. The resulting
predicate is just `A` (isinstance Iterable). Strings, which are Iterable, now enter the
element-wise iteration path instead of the scalar check path. This is TOF because the
entire `not isinstance(value, _str_type)` literal that forms part of the term is omitted,
making the surviving term weaker.

## Killing test

```text
tests/member1/test_member1.py::test_allowed_nfp_b_string_treated_as_scalar
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member1/test_member1.py::test_allowed_nfp_b_string_treated_as_scalar
```
