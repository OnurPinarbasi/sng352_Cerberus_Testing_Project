# Mutation F3-10

Fault class: ORF+

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
if isinstance(dependencies, _str_type) and not isinstance(
    dependencies, (Iterable, Mapping)
):
    dependencies = (dependencies,)
```

## Explanation

A∨¬B replaced by A∧¬B. Since `str` IS Iterable, `¬B = not isinstance(str,
(Iterable,Mapping))` = False. Therefore A∧¬B is always False for strings → string deps
are never normalised → the string is iterated character by character as separate field
names. This is ORF+: OR replaced with AND, making the condition impossible for string
inputs.

## Killing test

```text
tests/member3/test_member3.py::test_dep_orf_plus_multichar_dep
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member3/test_member3.py::test_dep_orf_plus_multichar_dep
```
