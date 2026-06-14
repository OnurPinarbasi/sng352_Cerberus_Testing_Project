# Mutation F3-1

Fault class: LIF

Target file: cerberus/validator.py  
Target function: _validate_empty

## Original predicate

```python
if isinstance(value, Sized) and len(value) == 0:
```

## Mutated predicate

```python
if True and len(value) == 0:
```

## Explanation

Clause A (`isinstance(value, Sized)`) is replaced with `True`. Non-Sized
values (e.g. integers) now reach `len(value)` which raises `TypeError`. This is LIF:
the isinstance guard is discarded by inserting a permanent true constant in its place.

## Killing test

```text
TODO: Any test passing a non-Sized type when the empty rule is present.
```

## How to apply

```bash
git apply mutation.patch
python -m pytest TODO: Any test passing a non-Sized type when the empty rule is present.
```
