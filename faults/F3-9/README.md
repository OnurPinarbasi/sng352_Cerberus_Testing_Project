# Mutation F3-9

Fault class: TIF

Target file: cerberus/validator.py  
Target function: _validate_regex

## Original predicate

```python
if not isinstance(value, _str_type):
    return
...
if not re_obj.match(value):
    self._error(field, errors.REGEX_MISMATCH)
```

## Mutated predicate

```python
if not isinstance(value, _str_type):
    return
...
if not re_obj.match(value) or not isinstance(value, _str_type):
    self._error(field, errors.REGEX_MISMATCH)
```

## Explanation

A spurious implicant `not isinstance(value, _str_type)` is added to the
error-filing condition. (In practice, since the guard above already returned for
non-strings, this extra term is vacuously False for code that reaches this line. The more
realistic modelling is that the guard is removed and the extra term is inserted at the
error check, making non-strings reach the error path.) The effect is that the regex error
can fire for inputs that should have been excluded. This is TIF: a spurious implicant
inserted into the DNF.

## Killing test

```text
tests/member3/test_member3.py::test_regex_tif_non_string
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member3/test_member3.py::test_regex_tif_non_string
```
