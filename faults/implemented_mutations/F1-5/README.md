# Mutation F1-5

Fault class: LNF

Target file: cerberus/validator.py  
Target function: __validate_dependencies_mapping

## Original predicate

```python
if not isinstance(dependency_values, Sequence) or isinstance(
    dependency_values, _str_type
):
    dependency_values = [dependency_values]
```

## Mutated predicate

```python
if isinstance(dependency_values, Sequence) or isinstance(
    dependency_values, _str_type
):
    dependency_values = [dependency_values]
```

## Explanation

The literal `not isinstance(dependency_values, Sequence)` (¬A) is negated
to `isinstance(dependency_values, Sequence)` (A). The normalisation logic is now inverted:
Sequence values (lists) are wrapped in another list (double-wrapped), while non-Sequence
scalars are used as-is. This is LNF because exactly one literal's polarity is flipped.

## Killing test

```text
tests/member1/test_member1.py::test_dep_mapping_list_dep_value_nfp
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member1/test_member1.py::test_dep_mapping_list_dep_value_nfp
```
