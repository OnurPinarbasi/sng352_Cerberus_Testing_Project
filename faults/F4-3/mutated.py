# Mutation F4-3 | Class: LNF | Target: _validate_contains
# Explanation: The literal `not isinstance(expected_values, Iterable)` (¬A) is negated to `isinstance(expected_values, Iterable)` (A). The normalisation branch no...
# Killing Test: tests/member4/test_member4.py::test_contains_list_expected_all_present
if isinstance(expected_values, Iterable) or isinstance(
    expected_values, _str_type
):
    expected_values = set((expected_values,))
else:
    expected_values = set(expected_values)
