# Mutation F3-4 | Class: TOF | Target: _validate_regex
# Explanation: The guard implicant `if not isinstance(value, _str_type): return` is entirely removed. This is a single-literal implicant (¬A) whose purpose is to ...
# Killing Test: tests/member3/test_member3.py::test_regex_nfp_a_non_string
def _validate_regex(self, pattern, field, value):
    """{'type': 'string'}"""
    if not pattern.endswith('$'):
        pattern += '$'
    re_obj = re.compile(pattern)
    if not re_obj.match(value):
        self._error(field, errors.REGEX_MISMATCH)
