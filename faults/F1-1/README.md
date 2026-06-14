# Mutation F1-1

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
matched = True and not isinstance(value, type_definition.excluded_types)
```

## Explanation

The literal `isinstance(value, type_definition.included_types)` (clause A)
is replaced with the constant `True`, effectively inserting an always-true literal that
short-circuits the included-types check. This is LIF because a new, spurious truth value
is injected into clause A of the conjunction, making it impossible for a wrong-type value
to fail the included-types test.

## Killing test

```text
tests/member1/test_member1.py::test_type_nfp_clause_a_false_error
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member1/test_member1.py::test_type_nfp_clause_a_false_error
```
