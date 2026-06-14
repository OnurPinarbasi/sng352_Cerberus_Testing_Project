if isinstance(value, Iterable):
    self._error(field, errors.MIN_LENGTH, len(value))