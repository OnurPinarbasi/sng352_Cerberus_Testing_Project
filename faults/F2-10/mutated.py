# Mutation F2-10 | Class: ORF* | Target: _validate_excludes
# Explanation: The conjunction A∧B is replaced by A∨B. The excluded field is now added to `_unrequired_by_excludes` whenever EITHER it exists in the schema OR the...
# Killing Test: tests/member2/test_member2.py::test_excludes_orf_star_required_missing
if excluded_field in self.schema or self.schema[field].get(
    'required', self.require_all
):
    self._unrequired_by_excludes.add(excluded_field)
