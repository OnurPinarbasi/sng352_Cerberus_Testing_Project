if isinstance(value, Iterable) and not isinstance(value, _str_type):
    unallowed = tuple(x for x in value if x not in allowed_values)