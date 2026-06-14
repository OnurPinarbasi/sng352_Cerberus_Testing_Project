# Mutation F3-2 | Class: LNF | Target: _validate_dependencies
# Explanation: The literal `not isinstance(dependencies, (Iterable, Mapping))` (¬B) is negated to `isinstance(dependencies, (Iterable, Mapping))` (B). The normali...
# Killing Test: tests/member3/test_member3.py::test_dep_list_dep_satisfied
if isinstance(dependencies, _str_type) or isinstance(
    dependencies, (Iterable, Mapping)
):
    dependencies = (dependencies,)
