# Mutation F1-2

Fault class: LIF

Target file: cerberus/validator.py  
Target function: _validate_type

## Original predicate

```python
matched = isinstance(
    value, type_definition.included_types
) and not isinstance(value, type_definition.excluded_types)
```

## Mutated predicate

```python
matched = isinstance(
    value, type_definition.included_types
) and True
```

## Explanation

The literal `not isinstance(value, type_definition.excluded_types)` (clause
¬B) is replaced with `True`. The excluded-types guard is deleted by inserting an
always-true constant in its place. Any value that matches `included_types` is now
considered valid even when it also matches `excluded_types`.

## Killing test

```text
tests/member1/test_member1.py::test_type_nfp_clause_b_true_error
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member1/test_member1.py::test_type_nfp_clause_b_true_error
```
