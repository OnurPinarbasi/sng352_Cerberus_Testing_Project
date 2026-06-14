except Exception as e:
    if not nullable and value is not None:
        self._error(field, error, str(e))
    return value