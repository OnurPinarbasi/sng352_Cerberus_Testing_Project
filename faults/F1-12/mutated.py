# Mutation F1-12 | Class: ENF | Target: _validate_allowed
# Explanation: The entire branch predicate is negated. Lists (Iterable, not str) now satisfy the negated condition as False → they go to the else/scalar branch. S...
# Killing Test: tests/member1/test_member1.py::test_allowed_enf_list_all_allowed
if not (isinstance(value, Iterable) and not isinstance(value, _str_type)):
    unallowed = tuple(x for x in value if x not in allowed_values)
    if unallowed:
        self._error(field, errors.UNALLOWED_VALUES, unallowed)
else:
    if value not in allowed_values:
        self._error(field, errors.UNALLOWED_VALUE, value)
