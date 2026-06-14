if not isinstance(dependency_values, Sequence) and isinstance(
    dependency_values, _str_type
):
    dependency_values = [dependency_values]