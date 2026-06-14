# Mutation F3-11 | Class: ORF* | Target: _validate_regex
# Explanation: The conjunction A∧¬B is replaced by A∨¬B. Since `value` has already been confirmed as a string (A=True always at this point), the OR condition is a...
# Killing Test: tests/member3/test_member3.py::test_regex_orf_star_string_matches
if isinstance(value, _str_type) or not re_obj.match(value):
    self._error(field, errors.REGEX_MISMATCH)
