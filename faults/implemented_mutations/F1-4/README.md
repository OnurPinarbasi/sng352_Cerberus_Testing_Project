# Mutation F1-4

Fault class: LIF

Target file: cerberus/validator.py  
Target function: _validate_minlength

## Original predicate

```python
if isinstance(value, Iterable) and len(value) < min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
```

## Mutated predicate

```python
if True and len(value) < min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
```

## Explanation

Clause A (`isinstance(value, Iterable)`) is replaced by the constant
`True`. The type guard that protects non-iterable values from having `len()` called on
them is eliminated. Passing an integer value now reaches `len(99)` which raises
`TypeError`, or (if the mutation is modelled as making the condition always true) any
value triggers a minlength check even when it cannot have a meaningful length.

## Killing test

```text
tests/member1/test_member1.py::test_minlength_nfp_a_non_iterable
```

## How to apply

```bash
git apply mutation.patch
python -m pytest tests/member1/test_member1.py::test_minlength_nfp_a_non_iterable
```
