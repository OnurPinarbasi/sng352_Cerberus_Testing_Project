if isinstance(value, Iterable):
    self._error(field, errors.MAX_LENGTH, len(value))