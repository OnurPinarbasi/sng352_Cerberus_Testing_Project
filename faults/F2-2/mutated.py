except Exception as e:
    if not (True and value is None):
        self._error(field, error, str(e))
    return value