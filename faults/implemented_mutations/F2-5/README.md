# Mutation F2-5

Fault class: LRF

Target file: cerberus/validator.py  
Target function: _validate_maxlength

## Original predicate

```python
if isinstance(value, Iterable) and len(value) > max_length:
    self._error(field, errors.MAX_LENGTH, len(value))
```

## Mutated predicate

```python
if isinstance(value, Iterable) and len(value) >= max_length:
    self._error(field, errors.MAX_LENGTH, len(value))
```

## Explanation

The relational operator `>` is replaced with `>=`. The boundary condition
is shifted: a value whose length exactly equals `max_length` now incorrectly triggers a
MAX_LENGTH error. This is LRF: a literal's comparison operator is replaced by a similar
but semantically different operator.

## Killing test

```text
tests/member2/test_member2.py::test_maxlength_nfp_b_within_limit
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member2/test_member2.py::test_maxlength_nfp_b_within_limit
```
