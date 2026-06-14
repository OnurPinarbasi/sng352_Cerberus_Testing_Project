# Mutation F4-7

Fault class: TNF

Target file: cerberus/validator.py  
Target function: _normalize_coerce

## Original predicate

```python
if field in schema and 'coerce' in schema[field]:
    mapping[field] = self.__normalize_coerce(
```

## Mutated predicate

```python
if not (field in schema and 'coerce' in schema[field]):
    mapping[field] = self.__normalize_coerce(
```

## Explanation

The implicant A∧B is negated to ¬A∨¬B. Coerce is now applied when the
field is absent from the schema OR when no coerce rule is defined — the exact inverse of
correct behaviour. Fields that have a coerce rule defined are not coerced; fields without
one are. This is TNF: the single implicant is fully negated.

## Killing test

```text
tests/member4/test_member4.py::test_normalize_coerce_tnf_with_coerce
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member4/test_member4.py::test_normalize_coerce_tnf_with_coerce
```
