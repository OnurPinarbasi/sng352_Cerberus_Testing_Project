# Mutation F2-4

Fault class: LIF

Target file: cerberus/validator.py  
Target function: _validate_readonly

## Original predicate

```python
if self._is_normalized and has_error:
    self._drop_remaining_rules()
```

## Mutated predicate

```python
if has_error:
    self._drop_remaining_rules()
```

## Explanation

The guard clause `self._is_normalized` (literal A) is dropped, collapsing
A∧B to just B. Remaining rules are now dropped whenever any readonly error has been
filed, regardless of whether normalization was performed. This is LIF: literal A was
removed (effectively replaced with implicit True), leaving only B.

## Killing test

```text
tests/member2/test_member2.py::test_readonly_unnormalized_errors
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member2/test_member2.py::test_readonly_unnormalized_errors
```
