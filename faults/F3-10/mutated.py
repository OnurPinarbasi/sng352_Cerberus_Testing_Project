# Mutation F3-10 | Class: ORF+ | Target: _validate_dependencies
# Explanation: A∨¬B replaced by A∧¬B. Since `str` IS Iterable, `¬B = not isinstance(str, (Iterable,Mapping))` = False. Therefore A∧¬B is always False for strings ...
# Killing Test: tests/member3/test_member3.py::test_dep_orf_plus_multichar_dep
if isinstance(dependencies, _str_type) and not isinstance(
    dependencies, (Iterable, Mapping)
):
    dependencies = (dependencies,)
