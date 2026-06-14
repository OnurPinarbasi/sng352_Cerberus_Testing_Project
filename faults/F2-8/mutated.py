# Mutation F2-8 | Class: TIF | Target: _validate_maxlength
# Explanation: A spurious implicant `not isinstance(value, Iterable)` (¬A) is inserted via OR. Non-iterable values now trigger a MAX_LENGTH error even though they...
# Killing Test: tests/member2/test_member2.py::test_maxlength_tif_non_iterable
if (isinstance(value, Iterable) and len(value) > max_length
        or not isinstance(value, Iterable)):
    self._error(field, errors.MAX_LENGTH, len(value))
