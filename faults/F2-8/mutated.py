if (isinstance(value, Iterable) and len(value) > max_length
        or not isinstance(value, Iterable)):
    self._error(field, errors.MAX_LENGTH, len(value))