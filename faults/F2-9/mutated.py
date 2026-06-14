# Mutation F2-9 | Class: ORF+ | Target: __normalize_coerce
# Explanation: The disjunction ¬A∨¬B is replaced by the conjunction ¬A∧¬B. The exception is now propagated only when BOTH `nullable=False` AND `value is not None`...
# Killing Test: tests/member2/test_member2.py::test_coerce_orf_plus_nullable_bad_coerce
except Exception as e:
    if not nullable and value is not None:
        self._error(field, error, str(e))
    return value
