# Mutation F4-1 | Class: TOF | Target: _validate_forbidden
# Explanation: The literal `not isinstance(value, _str_type)` (¬B) is omitted from the conjunction A∧¬B. The surviving predicate is just A (`isinstance(value, Seq...
# Killing Test: tests/member4/test_member4.py::test_forbidden_nfp_b_string_scalar_check
if isinstance(value, Sequence):
    forbidden = set(value) & set(forbidden_values)
    if forbidden:
        self._error(field, errors.FORBIDDEN_VALUES, list(forbidden))
else:
    if value in forbidden_values:
        self._error(field, errors.FORBIDDEN_VALUE, value)
