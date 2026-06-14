# Mutation F3-3

Fault class: LIF

Target file: cerberus/validator.py  
Target function: __validate_required_fields

## Original predicate

```python
missing = required - set(
    field
    for field in document
    if document.get(field) is not None or not self.ignore_none_values
)
```

## Mutated predicate

```python
missing = required - set(
    field
    for field in document
    if True or not self.ignore_none_values
)
```

## Explanation

The literal `document.get(field) is not None` (clause A) is replaced with
`True`. Every field present in the document now counts as "present with a value" regardless
of whether its value is `None`. When `ignore_none_values=True`, fields set to `None`
should not count as present; the mutation makes them always count, hiding required-field
violations. This is LIF: a true constant replaces clause A.

## Killing test

```text
tests/member3/test_member3.py::test_required_field_none_ignore_none_values
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member3/test_member3.py::test_required_field_none_ignore_none_values
```
