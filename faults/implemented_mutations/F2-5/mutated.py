if isinstance(value, Iterable) and len(value) >= max_length:
    self._error(field, errors.MAX_LENGTH, len(value))