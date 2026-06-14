# Mutation F2-8

Fault class: TIF

Target file: cerberus/validator.py  
Target function: _validate_maxlength

## Original predicate

```python
if isinstance(value, Iterable) and len(value) > max_length:
    self._error(field, errors.MAX_LENGTH, len(value))
```

## Mutated predicate

```python
if (isinstance(value, Iterable) and len(value) > max_length
        or not isinstance(value, Iterable)):
    self._error(field, errors.MAX_LENGTH, len(value))
```

## Explanation

A spurious implicant `not isinstance(value, Iterable)` (¬A) is inserted
via OR. Non-iterable values now trigger a MAX_LENGTH error even though they cannot
meaningfully have a length. This is TIF: an extra term is inserted into the DNF.

## Killing test

```text
tests/member2/test_member2.py::test_maxlength_tif_non_iterable
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member2/test_member2.py::test_maxlength_tif_non_iterable
```
