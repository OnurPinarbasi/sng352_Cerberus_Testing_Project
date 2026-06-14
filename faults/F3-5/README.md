# Mutation F3-5

Fault class: ENF

Target file: cerberus/validator.py  
Target function: _validate_regex

## Original predicate

```python
if not re_obj.match(value):
    self._error(field, errors.REGEX_MISMATCH)
```

## Mutated predicate

```python
if re_obj.match(value):
    self._error(field, errors.REGEX_MISMATCH)
```

## Explanation

The full predicate `not re_obj.match(value)` is negated by removing the
`not`. The error is now filed when the regex DOES match and withheld when it does NOT
match — the entire validation logic is inverted. This is ENF: the complete boolean
expression governing the error-filing decision is negated.

## Killing test

```text
tests/member3/test_member3.py::test_regex_utp_string_no_match
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member3/test_member3.py::test_regex_utp_string_no_match
```
