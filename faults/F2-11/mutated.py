# Mutation F2-11 | Class: ENF | Target: _validate_maxlength
# Explanation: The complete predicate is negated. The error now fires for values that are within the limit (the common valid case) and is suppressed for values th...
# Killing Test: tests/member2/test_member2.py::test_maxlength_enf_within_limit
if not (isinstance(value, Iterable) and len(value) > max_length):
    self._error(field, errors.MAX_LENGTH, len(value))
