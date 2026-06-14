# Mutation F2-2 | Class: LIF | Target: __normalize_coerce
# Explanation: The literal `nullable` (clause A) is replaced with the constant `True`. The field's nullable attribute is no longer consulted; the suppression path...
# Killing Test: tests/member2/test_member2.py::test_coerce_nonnullable_none_errors
except Exception as e:
    if not (True and value is None):
        self._error(field, error, str(e))
    return value
