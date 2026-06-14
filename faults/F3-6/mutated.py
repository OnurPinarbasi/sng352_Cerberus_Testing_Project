# Mutation F3-6 | Class: LDF | Target: _validate_empty
# Explanation: Literal B (`len(value) == 0`) is deleted. Any Sized value with `empty=False` triggers the EMPTY_NOT_ALLOWED error regardless of actual length. This...
# Killing Test: tests/member3/test_member3.py::test_empty_ldf_b_deleted
if isinstance(value, Sized):
