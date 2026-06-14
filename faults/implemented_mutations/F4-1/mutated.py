if isinstance(value, Sequence):
    forbidden = set(value) & set(forbidden_values)
    if forbidden:
        self._error(field, errors.FORBIDDEN_VALUES, list(forbidden))
else:
    if value in forbidden_values:
        self._error(field, errors.FORBIDDEN_VALUE, value)