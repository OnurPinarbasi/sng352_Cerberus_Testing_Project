# Mutation F4-6 | Class: LDF | Target: _normalize_coerce
# Explanation: Literal B (`'coerce' in schema[field]`) is deleted from the conjunction A∧B. Every field present in the schema now triggers a coerce call regardles...
# Killing Test: tests/member4/test_member4.py::test_normalize_coerce_ldf_no_coerce_key
if field in schema:
    mapping[field] = self.__normalize_coerce(
