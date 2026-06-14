if isinstance(value, Iterable) or len(value) < min_length:
    self._error(field, errors.MIN_LENGTH, len(value))