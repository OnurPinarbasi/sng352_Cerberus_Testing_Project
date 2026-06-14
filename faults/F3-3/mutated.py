missing = required - set(
    field
    for field in document
    if True or not self.ignore_none_values
)