if len(items) != len(values):
    self._error(field, errors.ITEMS_LENGTH, len(items), len(values))