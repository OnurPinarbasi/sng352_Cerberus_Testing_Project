def _validate_regex(self, pattern, field, value):
    """{'type': 'string'}"""
    if not isinstance(value, _str_type):
        return
    if not pattern.endswith('$'):
        pattern += '$'
    re_obj = re.compile(pattern)
    if not re_obj.match(value):
        self._error(field, errors.REGEX_MISMATCH)