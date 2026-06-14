# Mutation F2-1

Fault class: LNF

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
    if nullable and value is None:
        self._error(field, error, str(e))
    return value
```

## Explanation

The compound predicate `not (nullable and value is None)` (¬(A∧B)) is
negated to `nullable and value is None` (A∧B). The entire outer `not` is removed,
flipping the suppression logic. Errors that should be suppressed (nullable=True,
value=None) are now filed, and errors that should be propagated (all other cases) are now
swallowed. This is LNF: the outermost negation literal is flipped.

## Killing test

```text
tests/member2/test_member2.py::test_coerce_nullable_none_suppressed
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member2/test_member2.py::test_coerce_nullable_none_suppressed
```
