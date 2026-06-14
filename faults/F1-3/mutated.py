# Mutation F1-3 | Class: TOF | Target: _validate_allowed
# Explanation: The implicant `A ∧ ¬B` (isinstance Iterable AND NOT isinstance str) loses the `¬B` literal — the guard that diverts strings to the scalar path. The...
# Killing Test: tests/member1/test_member1.py::test_allowed_nfp_b_string_treated_as_scalar
if isinstance(value, Iterable):
    unallowed = tuple(x for x in value if x not in allowed_values)
    if unallowed:
        self._error(field, errors.UNALLOWED_VALUES, unallowed)
else:
    if value not in allowed_values:
        self._error(field, errors.UNALLOWED_VALUE, value)
