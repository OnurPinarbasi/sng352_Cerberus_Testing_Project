# Mutation F1-2 | Class: LIF | Target: _validate_type
# Explanation: The literal `not isinstance(value, type_definition.excluded_types)` (clause ¬B) is replaced with `True`. The excluded-types guard is deleted by ins...
# Killing Test: tests/member1/test_member1.py::test_type_nfp_clause_b_true_error
matched = isinstance(
    value, type_definition.included_types
) and True
