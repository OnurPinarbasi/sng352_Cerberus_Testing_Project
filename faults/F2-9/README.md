# Mutation F2-9

Fault class: ORF+

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
    if not nullable and value is not None:
        self._error(field, error, str(e))
    return value
```

## Explanation

The disjunction ¬A∨¬B is replaced by the conjunction ¬A∧¬B. The exception
is now propagated only when BOTH `nullable=False` AND `value is not None`. When
`nullable=True` and `value` is a non-None value that fails coerce, the exception is
incorrectly suppressed. This is ORF+: OR replaced with AND.

## Killing test

```text
tests/member2/test_member2.py::test_coerce_orf_plus_nullable_bad_coerce
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member2/test_member2.py::test_coerce_orf_plus_nullable_bad_coerce
```
