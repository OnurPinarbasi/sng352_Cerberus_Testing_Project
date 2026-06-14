# Mutation F3-11

Fault class: ORF*

Target file: cerberus/validator.py  
Target function: _validate_regex

## Original predicate

```python
if not re_obj.match(value):
    self._error(field, errors.REGEX_MISMATCH)
```

## Mutated predicate

```python
if isinstance(value, _str_type) or not re_obj.match(value):
    self._error(field, errors.REGEX_MISMATCH)
```

## Explanation

The conjunction A∧¬B is replaced by A∨¬B. Since `value` has already been
confirmed as a string (A=True always at this point), the OR condition is always True —
every string triggers a REGEX_MISMATCH error, including strings that correctly match the
pattern. This is ORF\*: AND replaced by OR.

## Killing test

```text
tests/member3/test_member3.py::test_regex_orf_star_string_matches
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member3/test_member3.py::test_regex_orf_star_string_matches
```
