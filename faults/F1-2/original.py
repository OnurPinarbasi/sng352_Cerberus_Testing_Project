matched = isinstance(
    value, type_definition.included_types
) and not isinstance(value, type_definition.excluded_types)