# Mutation F3-7

Fault class: LRF

Target file: cerberus/validator.py  
Target function: _validate_empty

## Original predicate

```python
if isinstance(value, Sized) and len(value) == 0:
```

## Mutated predicate

```python
if isinstance(value, Sized) and len(value) == 1:
```

## Explanation

The constant `0` in the equality `len(value) == 0` is replaced with `1`.
Single-element containers now trigger the empty-not-allowed error while truly empty
containers escape it. This is LRF: a numeric constant literal is replaced with a similar
but wrong value.

## Killing test

```text
tests/member3/test_member3.py::test_empty_lrf_single_element
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member3/test_member3.py::test_empty_lrf_single_element
```
