# Mutation F4-8 | Class: TIF | Target: _validate_forbidden
# Explanation: A spurious implicant `isinstance(value, int)` is inserted via OR. Integers now enter the list-iteration branch → `set(42)` → `TypeError`. This is T...
# Killing Test: tests/member4/test_member4.py::test_forbidden_tif_integer_not_forbidden
if (isinstance(value, Sequence) and not isinstance(value, _str_type)
        or isinstance(value, int)):
    forbidden = set(value) & set(forbidden_values)
