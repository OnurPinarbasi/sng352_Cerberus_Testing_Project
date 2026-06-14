# Mutation F3-9 | Class: TIF | Target: _validate_regex
# Explanation: A spurious implicant `not isinstance(value, _str_type)` is added to the error-filing condition. (In practice, since the guard above already returne...
# Killing Test: tests/member3/test_member3.py::test_regex_tif_non_string
if not re_obj.match(value) or not isinstance(value, _str_type):
    self._error(field, errors.REGEX_MISMATCH)
