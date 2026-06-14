missing = required - set(
    field
    for field in document
    if document.get(field) is not None or not self.ignore_none_values
)