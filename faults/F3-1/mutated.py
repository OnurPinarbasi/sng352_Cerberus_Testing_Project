# Mutation F3-1 | Class: LIF | Target: _validate_empty
# Explanation: Clause A (`isinstance(value, Sized)`) is replaced with `True`. Non-Sized values (e.g. integers) now reach `len(value)` which raises `TypeError`. Th...
# Killing Test: 
if True and len(value) == 0:
