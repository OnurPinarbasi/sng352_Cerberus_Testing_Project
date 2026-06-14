# Mutation F2-3

Fault class: TOF

Target file: cerberus/validator.py  
Target function: _validate_excludes

## Original predicate

```python
for excluded_field in excluded_fields:
    if excluded_field in self.schema and self.schema[field].get(
        'required', self.require_all
    ):
        self._unrequired_by_excludes.add(excluded_field)
```

## Mutated predicate

```python
for excluded_field in excluded_fields:
    if excluded_field in self.schema:
        self._unrequired_by_excludes.add(excluded_field)
```

## Explanation

The entire second clause `self.schema[field].get('required',
self.require_all)` (literal B) is omitted from the conjunction A∧B. The predicate
collapses to just A (`excluded_field in self.schema`). Any schema-defined excluded field
is now unconditionally added to `_unrequired_by_excludes`, even when the excluding field
is not actually marked required. This is TOF: literal B is dropped, weakening the term.

## Killing test

```text
tests/member2/test_member2.py::test_excludes_neither_present_required_fails
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member2/test_member2.py::test_excludes_neither_present_required_fails
```
