# Mutation F4-6

Fault class: LDF

Target file: cerberus/validator.py  
Target function: _normalize_coerce

## Original predicate

```python
if field in schema and 'coerce' in schema[field]:
    mapping[field] = self.__normalize_coerce(
```

## Mutated predicate

```python
if field in schema:
    mapping[field] = self.__normalize_coerce(
```

## Explanation

Literal B (`'coerce' in schema[field]`) is deleted from the conjunction
A∧B. Every field present in the schema now triggers a coerce call regardless of whether
a coerce rule was defined. Accessing `schema[field]['coerce']` when the key is absent
raises `KeyError`. This is LDF: literal B is removed.

## Killing test

```text
tests/member4/test_member4.py::test_normalize_coerce_ldf_no_coerce_key
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member4/test_member4.py::test_normalize_coerce_ldf_no_coerce_key
```
