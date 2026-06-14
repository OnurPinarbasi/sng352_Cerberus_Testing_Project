if not isinstance(expected_values, Iterable) and isinstance(
    expected_values, _str_type
):
    expected_values = set((expected_values,))
else:
    expected_values = set(expected_values)