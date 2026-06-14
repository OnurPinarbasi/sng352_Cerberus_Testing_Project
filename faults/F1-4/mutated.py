# Mutation F1-4 | Class: LIF | Target: _validate_minlength
# Explanation: Clause A (`isinstance(value, Iterable)`) is replaced by the constant `True`. The type guard that protects non-iterable values from having `len()` c...
# Killing Test: tests/member1/test_member1.py::test_minlength_nfp_a_non_iterable
if True and len(value) < min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
