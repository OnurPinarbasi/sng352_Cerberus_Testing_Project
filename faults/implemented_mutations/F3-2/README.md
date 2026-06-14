# Mutation F3-2

Fault class: LNF

Target file: cerberus/validator.py  
Target function: _validate_dependencies

## Original predicate

```python
if isinstance(dependencies, _str_type) or not isinstance(
    dependencies, (Iterable, Mapping)
):
    dependencies = (dependencies,)
```

## Mutated predicate

```python
if isinstance(dependencies, _str_type) or isinstance(
    dependencies, (Iterable, Mapping)
):
    dependencies = (dependencies,)
```

## Explanation

The literal `not isinstance(dependencies, (Iterable, Mapping))` (¬B) is
negated to `isinstance(dependencies, (Iterable, Mapping))` (B). The normalisation now
wraps lists and mappings (which should pass through as-is) in a tuple, and leaves scalars
(which should be normalised) unwrapped. This is LNF: one literal's negation is flipped.

## Killing test

```text
tests/member3/test_member3.py::test_dep_list_dep_satisfied
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member3/test_member3.py::test_dep_list_dep_satisfied
```
