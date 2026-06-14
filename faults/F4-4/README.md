# Mutation F4-4

Fault class: LIF

Target file: cerberus/validator.py  
Target function: _normalize_coerce

## Original predicate

```python
if field in schema and 'coerce' in schema[field]:
    mapping[field] = self.__normalize_coerce(
```

## Mutated predicate

```python
if field in schema and True:
    mapping[field] = self.__normalize_coerce(
```

## Explanation

The literal `'coerce' in schema[field]` (clause B) is replaced with the
constant `True`. Every field present in the schema now unconditionally triggers the
`__normalize_coerce` call, even fields that have no `coerce` rule defined. The coerce
processor would be `None` → `None(value)` → `TypeError`. This is LIF: literal B is
replaced by an always-true constant.

## Killing test

```text
tests/member4/test_member4.py::test_normalize_coerce_no_coerce_rule
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member4/test_member4.py::test_normalize_coerce_no_coerce_rule
```
