# Mutation F4-11

Fault class: ENF

Target file: cerberus/validator.py  
Target function: _validate_forbidden

## Original predicate

```python
if isinstance(value, Sequence) and not isinstance(value, _str_type):
    forbidden = set(value) & set(forbidden_values)
    if forbidden:
        self._error(field, errors.FORBIDDEN_VALUES, list(forbidden))
else:
    if value in forbidden_values:
        self._error(field, errors.FORBIDDEN_VALUE, value)
```

## Mutated predicate

```python
if not (isinstance(value, Sequence) and not isinstance(value, _str_type)):
    forbidden = set(value) & set(forbidden_values)
    if forbidden:
        self._error(field, errors.FORBIDDEN_VALUES, list(forbidden))
else:
    if value in forbidden_values:
        self._error(field, errors.FORBIDDEN_VALUE, value)
```

## Explanation

The complete branch predicate is negated. Lists now satisfy the negated
condition as False → they fall to the else (scalar) branch → `list in forbidden_values`
is False (a list object is never equal to the scalar forbidden values) → forbidden list
elements pass undetected. This is ENF: the entire governing predicate is negated.

## Killing test

```text
tests/member4/test_member4.py::test_forbidden_enf_list_with_forbidden
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member4/test_member4.py::test_forbidden_enf_list_with_forbidden
```
