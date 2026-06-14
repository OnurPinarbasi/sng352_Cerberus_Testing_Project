# Mutation F3-8 | Class: TNF | Target: _validate_empty
# Explanation: Implicant A∧B negated to ¬A∨¬B. The error fires for non-Sized values or for non-empty containers — the exact inverse of the intended test for empti...
# Killing Test: tests/member3/test_member3.py::test_empty_tnf_non_empty
if not isinstance(value, Sized) or len(value) != 0:
