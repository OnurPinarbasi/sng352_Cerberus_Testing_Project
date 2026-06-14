for excluded_field in excluded_fields:
    if excluded_field in self.schema:
        self._unrequired_by_excludes.add(excluded_field)