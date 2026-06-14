# Mutation F1-10

Fault class: ORF+

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
if not isinstance(dependency_values, Sequence) and isinstance(
    dependency_values, _str_type
):
    dependency_values = [dependency_values]
```

## Explanation

The disjunction `¬A ∨ B` is replaced by the conjunction `¬A ∧ B`. Since
`str` IS a `Sequence`, `¬A` is False for strings → `¬A ∧ B` is always False. No
dependency value is ever normalised. Integers, strings, and other non-list values are used
raw in the membership check, causing `TypeError` or incorrect comparisons. This is ORF+:
the OR operator is replaced by AND, strengthening the condition into one that is never
satisfied.

## Killing test

```text
tests/member1/test_member1.py::test_dep_mapping_orf_plus_int_dep
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member1/test_member1.py::test_dep_mapping_orf_plus_int_dep
```
