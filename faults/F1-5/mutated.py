# Mutation F1-5 | Class: LNF | Target: __validate_dependencies_mapping
# Explanation: The literal `not isinstance(dependency_values, Sequence)` (¬A) is negated to `isinstance(dependency_values, Sequence)` (A). The normalisation logic...
# Killing Test: tests/member1/test_member1.py::test_dep_mapping_list_dep_value_nfp
if isinstance(dependency_values, Sequence) or isinstance(
    dependency_values, _str_type
):
    dependency_values = [dependency_values]
