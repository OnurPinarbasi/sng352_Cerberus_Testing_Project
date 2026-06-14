# Mutation F3-5 | Class: ENF | Target: _validate_regex
# Explanation: The full predicate `not re_obj.match(value)` is negated by removing the `not`. The error is now filed when the regex DOES match and withheld when i...
# Killing Test: tests/member3/test_member3.py::test_regex_utp_string_no_match
if re_obj.match(value):
    self._error(field, errors.REGEX_MISMATCH)
