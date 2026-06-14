# Mutation F4-4 | Class: LIF | Target: _normalize_coerce
# Explanation: The literal `'coerce' in schema[field]` (clause B) is replaced with the constant `True`. Every field present in the schema now unconditionally trig...
# Killing Test: tests/member4/test_member4.py::test_normalize_coerce_no_coerce_rule
if field in schema and True:
    mapping[field] = self.__normalize_coerce(
