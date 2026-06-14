# Mutation F2-5 | Class: LRF | Target: _validate_maxlength
# Explanation: The relational operator `>` is replaced with `>=`. The boundary condition is shifted: a value whose length exactly equals `max_length` now incorrec...
# Killing Test: tests/member2/test_member2.py::test_maxlength_nfp_b_within_limit
if isinstance(value, Iterable) and len(value) >= max_length:
    self._error(field, errors.MAX_LENGTH, len(value))
