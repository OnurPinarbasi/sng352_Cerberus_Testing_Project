# Mutation F1-11 | Class: ORF* | Target: _validate_minlength
# Explanation: The conjunction A∧B is replaced by the disjunction A∨B. The error now fires whenever the value is iterable (regardless of length) OR whenever the v...
# Killing Test: tests/member1/test_member1.py::test_minlength_orf_star_long_list
if isinstance(value, Iterable) or len(value) < min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
