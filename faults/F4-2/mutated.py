# Mutation F4-2 | Class: LNF | Target: _validate_schema
# Explanation: The literal `not isinstance(value, _str_type)` (¬B) is negated to `isinstance(value, _str_type)` (B). Now a list never satisfies A∧B (since a list ...
# Killing Test: tests/member4/test_member4.py::test_schema_sequence_value_invalid
if isinstance(value, Sequence) and isinstance(value, _str_type):
    self.__validate_schema_sequence(field, schema, value)
elif isinstance(value, Mapping):
    self.__validate_schema_mapping(field, schema, value)
