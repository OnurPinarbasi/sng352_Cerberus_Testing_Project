# Mutation F1-12

Fault class: ENF

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
if not (isinstance(value, Iterable) and not isinstance(value, _str_type)):
    unallowed = tuple(x for x in value if x not in allowed_values)
    if unallowed:
        self._error(field, errors.UNALLOWED_VALUES, unallowed)
else:
    if value not in allowed_values:
        self._error(field, errors.UNALLOWED_VALUE, value)
```

## Explanation

The entire branch predicate is negated. Lists (Iterable, not str) now
satisfy the negated condition as False → they go to the else/scalar branch. Scalars and
strings (which do not satisfy the original) now enter the list-iteration branch.
This is ENF: the complete governing boolean expression is negated.

## Killing test

```text
tests/member1/test_member1.py::test_allowed_enf_list_all_allowed
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member1/test_member1.py::test_allowed_enf_list_all_allowed
```
