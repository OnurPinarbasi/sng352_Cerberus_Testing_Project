if re_obj.match(value):
    self._error(field, errors.REGEX_MISMATCH)