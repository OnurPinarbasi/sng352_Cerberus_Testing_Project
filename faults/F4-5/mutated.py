# Mutation F4-5 | Class: LRF | Target: _validate_items
# Explanation: The relational operator `!=` is replaced with `==`. The length mismatch error now fires when lengths are EQUAL and is suppressed when they DIFFER —...
# Killing Test: tests/member4/test_member4.py::test_items_length_mismatch
if len(items) == len(values):
    self._error(field, errors.ITEMS_LENGTH, len(items), len(values))
