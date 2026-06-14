# Mutation F1-10 | Class: ORF+ | Target: __validate_dependencies_mapping
# Explanation: The disjunction `¬A ∨ B` is replaced by the conjunction `¬A ∧ B`. Since `str` IS a `Sequence`, `¬A` is False for strings → `¬A ∧ B` is always False...
# Killing Test: tests/member1/test_member1.py::test_dep_mapping_orf_plus_int_dep
if not isinstance(dependency_values, Sequence) and isinstance(
    dependency_values, _str_type
):
    dependency_values = [dependency_values]
