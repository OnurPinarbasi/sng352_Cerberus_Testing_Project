for excluded_field in excluded_fields:
    if excluded_field in self.schema and self.schema[field].get(
        'required', self.require_all
    ):
        self._unrequired_by_excludes.add(excluded_field)