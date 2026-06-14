# Mutation F2-10

Fault class: ORF*

Target file: cerberus/validator.py  
Target function: _validate_excludes

## Original predicate

```python
if excluded_field in self.schema and self.schema[field].get(
    'required', self.require_all
):
    self._unrequired_by_excludes.add(excluded_field)
```

## Mutated predicate

```python
if excluded_field in self.schema or self.schema[field].get(
    'required', self.require_all
):
    self._unrequired_by_excludes.add(excluded_field)
```

## Explanation

The conjunction A∧B is replaced by A∨B. The excluded field is now added
to `_unrequired_by_excludes` whenever EITHER it exists in the schema OR the excluding
field is required — rather than both conditions needing to be true. Required fields can
be silently exempted from the required check even when the excluding field is not itself
required. This is ORF\*: AND replaced with OR.

## Killing test

```text
tests/member2/test_member2.py::test_excludes_orf_star_required_missing
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member2/test_member2.py::test_excludes_orf_star_required_missing
```
