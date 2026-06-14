except Exception as e:
    if not (nullable and value is None):
        self._error(field, error, str(e))
    return value