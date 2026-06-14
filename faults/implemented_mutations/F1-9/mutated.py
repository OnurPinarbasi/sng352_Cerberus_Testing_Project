if (isinstance(value, Iterable) and not isinstance(value, _str_type)
        or isinstance(value, int)):
    unallowed = tuple(x for x in value if x not in allowed_values)