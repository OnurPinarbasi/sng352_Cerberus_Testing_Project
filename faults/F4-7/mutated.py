if not (field in schema and 'coerce' in schema[field]):
    mapping[field] = self.__normalize_coerce(