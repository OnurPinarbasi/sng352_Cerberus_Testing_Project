# Mutation F1-9 | Class: TIF | Target: _validate_allowed
# Explanation: A spurious new implicant `isinstance(value, int)` is inserted into the DNF via OR. Integers now enter the list-iteration branch even though the ori...
# Killing Test: tests/member1/test_member1.py::test_allowed_tif_integer_in_allowed
if (isinstance(value, Iterable) and not isinstance(value, _str_type)
        or isinstance(value, int)):
    unallowed = tuple(x for x in value if x not in allowed_values)
