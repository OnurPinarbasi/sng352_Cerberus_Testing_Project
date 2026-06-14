# Mutation F2-4 | Class: LIF | Target: _validate_readonly
# Explanation: The guard clause `self._is_normalized` (literal A) is dropped, collapsing A∧B to just B. Remaining rules are now dropped whenever any readonly erro...
# Killing Test: tests/member2/test_member2.py::test_readonly_unnormalized_errors
if has_error:
    self._drop_remaining_rules()
