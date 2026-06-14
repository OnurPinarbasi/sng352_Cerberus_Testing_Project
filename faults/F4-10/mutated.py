# Mutation F4-10 | Class: ORF* | Target: _validate_forbidden
# Explanation: A∧¬B replaced by A∨¬B. For integers: A=False, ¬B=True (integer is not a string) → `False∨True` = True → integers enter the list-iteration branch → ...
# Killing Test: tests/member4/test_member4.py::test_forbidden_orf_star_integer
if isinstance(value, Sequence) or not isinstance(value, _str_type):
