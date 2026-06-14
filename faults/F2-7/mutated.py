# Mutation F2-7 | Class: TNF | Target: _validate_maxlength
# Explanation: A∧B negated to ¬A∨¬B. The error now fires when the value is NOT iterable OR when it is within the limit — the complete inverse of intended behaviou...
# Killing Test: tests/member2/test_member2.py::test_maxlength_tnf_within_limit
if not isinstance(value, Iterable) or len(value) <= max_length:
    self._error(field, errors.MAX_LENGTH, len(value))
