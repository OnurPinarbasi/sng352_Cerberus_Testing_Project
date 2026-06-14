# Mutation F1-8 | Class: TNF | Target: _validate_minlength
# Explanation: The single implicant A∧B is negated to ¬(A∧B) = ¬A∨¬B. The error now fires when the value is NOT iterable OR when its length already meets the mini...
# Killing Test: tests/member1/test_member1.py::test_minlength_tnf_long_list
if not isinstance(value, Iterable) or len(value) >= min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
