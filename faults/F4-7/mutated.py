# Mutation F4-7 | Class: TNF | Target: _normalize_coerce
# Explanation: The implicant A∧B is negated to ¬A∨¬B. Coerce is now applied when the field is absent from the schema OR when no coerce rule is defined — the exact...
# Killing Test: tests/member4/test_member4.py::test_normalize_coerce_tnf_with_coerce
if not (field in schema and 'coerce' in schema[field]):
    mapping[field] = self.__normalize_coerce(
