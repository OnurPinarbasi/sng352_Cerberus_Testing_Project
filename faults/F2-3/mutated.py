# Mutation F2-3 | Class: TOF | Target: _validate_excludes
# Explanation: The entire second clause `self.schema[field].get('required', self.require_all)` (literal B) is omitted from the conjunction A∧B. The predicate coll...
# Killing Test: tests/member2/test_member2.py::test_excludes_neither_present_required_fails
for excluded_field in excluded_fields:
    if excluded_field in self.schema:
        self._unrequired_by_excludes.add(excluded_field)
