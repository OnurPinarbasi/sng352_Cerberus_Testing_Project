# Mutation F2-1 | Class: LNF | Target: __normalize_coerce
# Explanation: The compound predicate `not (nullable and value is None)` (¬(A∧B)) is negated to `nullable and value is None` (A∧B). The entire outer `not` is remo...
# Killing Test: tests/member2/test_member2.py::test_coerce_nullable_none_suppressed
except Exception as e:
    if nullable and value is None:
        self._error(field, error, str(e))
    return value
