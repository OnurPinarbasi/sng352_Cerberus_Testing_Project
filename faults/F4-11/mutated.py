# Mutation F4-11 | Class: ENF | Target: _validate_forbidden
# Explanation: The complete branch predicate is negated. Lists now satisfy the negated condition as False → they fall to the else (scalar) branch → `list in forbi...
# Killing Test: tests/member4/test_member4.py::test_forbidden_enf_list_with_forbidden
if not (isinstance(value, Sequence) and not isinstance(value, _str_type)):
    forbidden = set(value) & set(forbidden_values)
    if forbidden:
        self._error(field, errors.FORBIDDEN_VALUES, list(forbidden))
else:
    if value in forbidden_values:
        self._error(field, errors.FORBIDDEN_VALUE, value)
