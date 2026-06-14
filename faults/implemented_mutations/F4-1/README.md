# Mutation F4-1

Fault class: TOF

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
if isinstance(value, Sequence):
    forbidden = set(value) & set(forbidden_values)
    if forbidden:
        self._error(field, errors.FORBIDDEN_VALUES, list(forbidden))
else:
    if value in forbidden_values:
        self._error(field, errors.FORBIDDEN_VALUE, value)
```

## Explanation

The literal `not isinstance(value, _str_type)` (¬B) is omitted from the
conjunction A∧¬B. The surviving predicate is just A (`isinstance(value, Sequence)`).
Strings (which are Sequences) now enter the element-wise path and have each character
checked against the forbidden values, instead of being checked as a scalar. This is TOF:
the ¬B literal is omitted, weakening the gate term.

## Killing test

```text
tests/member4/test_member4.py::test_forbidden_nfp_b_string_scalar_check
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member4/test_member4.py::test_forbidden_nfp_b_string_scalar_check
```
