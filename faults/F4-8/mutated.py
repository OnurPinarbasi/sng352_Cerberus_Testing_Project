if (isinstance(value, Sequence) and not isinstance(value, _str_type)
        or isinstance(value, int)):
    forbidden = set(value) & set(forbidden_values)