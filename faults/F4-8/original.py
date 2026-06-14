if isinstance(value, Sequence) and not isinstance(value, _str_type):
    forbidden = set(value) & set(forbidden_values)