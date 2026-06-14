if isinstance(value, Sequence) and isinstance(value, _str_type):
    self.__validate_schema_sequence(field, schema, value)
elif isinstance(value, Mapping):
    self.__validate_schema_mapping(field, schema, value)