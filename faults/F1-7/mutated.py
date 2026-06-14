# Mutation F1-7 | Class: LRF | Target: _validate_minlength
# Explanation: The strict-less-than operator `<` in literal B is replaced with `<=`. A value whose length exactly equals `min_length` now incorrectly triggers a M...
# Killing Test: tests/member1/test_member1.py::test_minlength_lrf_boundary
if isinstance(value, Iterable) and len(value) <= min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
