# Mutation F3-7 | Class: LRF | Target: _validate_empty
# Explanation: The constant `0` in the equality `len(value) == 0` is replaced with `1`. Single-element containers now trigger the empty-not-allowed error while tr...
# Killing Test: tests/member3/test_member3.py::test_empty_lrf_single_element
if isinstance(value, Sized) and len(value) == 1:
