# Mutation F4-2

Fault class: LNF

Target file: cerberus/validator.py  
Target function: _validate_schema

## Original predicate

```python
if isinstance(value, Sequence) and not isinstance(value, _str_type):
    self.__validate_schema_sequence(field, schema, value)
elif isinstance(value, Mapping):
    self.__validate_schema_mapping(field, schema, value)
```

## Mutated predicate

```python
if isinstance(value, Sequence) and isinstance(value, _str_type):
    self.__validate_schema_sequence(field, schema, value)
elif isinstance(value, Mapping):
    self.__validate_schema_mapping(field, schema, value)
```

## Explanation

The literal `not isinstance(value, _str_type)` (¬B) is negated to
`isinstance(value, _str_type)` (B). Now a list never satisfies A∧B (since a list is not
a string) and the sequence validation path becomes dead code. Lists fall through both
`if` and `elif` without any validation. This is LNF: one literal's polarity is flipped.

## Killing test

```text
tests/member4/test_member4.py::test_schema_sequence_value_invalid
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member4/test_member4.py::test_schema_sequence_value_invalid
```
