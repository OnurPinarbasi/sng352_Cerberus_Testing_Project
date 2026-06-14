# Mutation F1-6 | Class: LDF | Target: _validate_minlength
# Explanation: Literal B (`len(value) < min_length`) is deleted from the conjunction A∧B. The surviving predicate is A alone (`isinstance(value, Iterable)`). Any ...
# Killing Test: tests/member1/test_member1.py::test_minlength_ldf_b_deleted
if isinstance(value, Iterable):
    self._error(field, errors.MIN_LENGTH, len(value))
