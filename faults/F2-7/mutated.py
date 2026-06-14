if not isinstance(value, Iterable) or len(value) <= max_length:
    self._error(field, errors.MAX_LENGTH, len(value))