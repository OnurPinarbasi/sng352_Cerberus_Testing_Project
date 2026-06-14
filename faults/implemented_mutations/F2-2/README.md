# Mutation F2-2

Fault class: LIF

Target file: cerberus/validator.py  
Target function: __normalize_coerce

## Original predicate

```python
except Exception as e:
    if not (nullable and value is None):
        self._error(field, error, str(e))
    return value
```

## Mutated predicate

```python
except Exception as e:
    if not (True and value is None):
        self._error(field, error, str(e))
    return value
```

## Explanation

The literal `nullable` (clause A) is replaced with the constant `True`.
The field's nullable attribute is no longer consulted; the suppression path is taken
whenever `value is None` regardless of whether nullability is permitted. This is LIF:
a spurious always-true literal is inserted in place of clause A.

## Killing test

```text
tests/member2/test_member2.py::test_coerce_nonnullable_none_errors
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member2/test_member2.py::test_coerce_nonnullable_none_errors
```
