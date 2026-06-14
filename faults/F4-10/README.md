# Mutation F4-10

Fault class: ORF*

Target file: cerberus/validator.py  
Target function: _validate_forbidden

## Original predicate

```python
if isinstance(value, Sequence) and not isinstance(value, _str_type):
```

## Mutated predicate

```python
if isinstance(value, Sequence) or not isinstance(value, _str_type):
```

## Explanation

A∧¬B replaced by A∨¬B. For integers: A=False, ¬B=True (integer is not a
string) → `False∨True` = True → integers enter the list-iteration branch → `set(42)` →
`TypeError`. This is ORF\*: AND replaced by OR.

## Killing test

```text
tests/member4/test_member4.py::test_forbidden_orf_star_integer
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member4/test_member4.py::test_forbidden_orf_star_integer
```
