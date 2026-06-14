# Mutation F4-9 | Class: ORF+ | Target: _validate_contains
# Explanation: ¬A∨B replaced by ¬A∧B. Since `str` IS Iterable, `¬A=False` for strings → `¬A∧B` is always False. Strings fall to the else branch → `set('abc')` = `...
# Killing Test: tests/member4/test_member4.py::test_contains_orf_plus_string_multi
if not isinstance(expected_values, Iterable) and isinstance(
    expected_values, _str_type
):
    expected_values = set((expected_values,))
else:
    expected_values = set(expected_values)
