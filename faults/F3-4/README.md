# Mutation F3-4

Fault class: TOF

Target file: cerberus/validator.py  
Target function: _validate_regex

## Original predicate

```python
def _validate_regex(self, pattern, field, value):
    """{'type': 'string'}"""
    if not isinstance(value, _str_type):
        return
    if not pattern.endswith('$'):
        pattern += '$'
    re_obj = re.compile(pattern)
    if not re_obj.match(value):
        self._error(field, errors.REGEX_MISMATCH)
```

## Mutated predicate

```python
def _validate_regex(self, pattern, field, value):
    """{'type': 'string'}"""
    if not pattern.endswith('$'):
        pattern += '$'
    re_obj = re.compile(pattern)
    if not re_obj.match(value):
        self._error(field, errors.REGEX_MISMATCH)
```

## Explanation

The guard implicant `if not isinstance(value, _str_type): return` is
entirely removed. This is a single-literal implicant (¬A) whose purpose is to skip regex
checking for non-string values. Its removal means `re_obj.match(value)` is called on
integers, lists, etc. → `TypeError`. This is TOF: the entire guard term is omitted.

## Killing test

```text
tests/member3/test_member3.py::test_regex_nfp_a_non_string
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member3/test_member3.py::test_regex_nfp_a_non_string
```
