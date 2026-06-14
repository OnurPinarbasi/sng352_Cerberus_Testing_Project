if not isinstance(value, _str_type):
    return
...
if not re_obj.match(value) or not isinstance(value, _str_type):
    self._error(field, errors.REGEX_MISMATCH)