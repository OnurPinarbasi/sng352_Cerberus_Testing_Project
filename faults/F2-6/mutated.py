# Mutation F2-6 | Class: LDF | Target: _validate_maxlength
# Explanation: Literal B (`len(value) > max_length`) is deleted from the conjunction A∧B. Any iterable value now triggers MAX_LENGTH, regardless of its actual len...
# Killing Test: tests/member2/test_member2.py::test_maxlength_ldf_b_deleted
if isinstance(value, Iterable):
    self._error(field, errors.MAX_LENGTH, len(value))
