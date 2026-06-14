# Mutation F3-3 | Class: LIF | Target: __validate_required_fields
# Explanation: The literal `document.get(field) is not None` (clause A) is replaced with `True`. Every field present in the document now counts as "present with a...
# Killing Test: tests/member3/test_member3.py::test_required_field_none_ignore_none_values
missing = required - set(
    field
    for field in document
    if True or not self.ignore_none_values
)
