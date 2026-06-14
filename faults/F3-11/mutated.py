if isinstance(value, _str_type) or not re_obj.match(value):
    self._error(field, errors.REGEX_MISMATCH)