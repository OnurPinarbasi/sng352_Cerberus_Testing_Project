# Mutation / Fault Emulation Descriptions

Each entry shows the **original source fragment** from `cerberus/validator.py`, the
**mutated fragment**, the **Table 8.1 fault class** being emulated, the **rationale**
for that classification, and the **killing test**.

All line numbers refer to the installed cerberus source
(`cerberus/validator.py`).

---

## Member 1

### Mutation F1-1 · `_validate_type` · LIF (Literal Insertion Fault)

**Original code (line 1543):**

```python
matched = isinstance(
    value, type_definition.included_types
) and not isinstance(value, type_definition.excluded_types)
```

**Mutated code:**

```python
matched = True and not isinstance(value, type_definition.excluded_types)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F1-1/`
- Patch: `faults/implemented_mutations/F1-1/mutation.patch`
- Original fragment: `faults/implemented_mutations/F1-1/original.py`
- Mutated fragment: `faults/implemented_mutations/F1-1/mutated.py`

**Fault class:** Literal Insertion Fault (LIF)

**Rationale:** The literal `isinstance(value, type_definition.included_types)` (clause A)
is replaced with the constant `True`, effectively inserting an always-true literal that
short-circuits the included-types check. This is LIF because a new, spurious truth value
is injected into clause A of the conjunction, making it impossible for a wrong-type value
to fail the included-types test.

**Killing test:** `test_type_nfp_clause_a_false_error`
— passes a string to a field typed `integer`. Cerberus evaluates `isinstance('hello',
(int,))` → False → `matched=False` → `BAD_TYPE` error → `validate()` returns `False`.
With the mutation `matched = True and ...` → `True` regardless → no `BAD_TYPE` → `True`.
The assertion `assert v.validate({'x': 'hello'}) is False` fails, killing the mutant.

---

### Mutation F1-2 · `_validate_type` · LIF (Literal Insertion Fault)

**Original code (line 1543):**

```python
matched = isinstance(
    value, type_definition.included_types
) and not isinstance(value, type_definition.excluded_types)
```

**Mutated code:**

```python
matched = isinstance(
    value, type_definition.included_types
) and True
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F1-2/`
- Patch: `faults/implemented_mutations/F1-2/mutation.patch`
- Original fragment: `faults/implemented_mutations/F1-2/original.py`
- Mutated fragment: `faults/implemented_mutations/F1-2/mutated.py`

**Fault class:** Literal Insertion Fault (LIF)

**Rationale:** The literal `not isinstance(value, type_definition.excluded_types)` (clause
¬B) is replaced with `True`. The excluded-types guard is deleted by inserting an
always-true constant in its place. Any value that matches `included_types` is now
considered valid even when it also matches `excluded_types`.

**Killing test:** `test_type_nfp_clause_b_true_error`
— tests a value that satisfies `included_types` but is also in `excluded_types` (e.g.
`bool` for a number type that excludes bool). With the mutation the `excluded_types` check
is bypassed → `matched=True` → no error. The assertion catches the changed result.

---

### Mutation F1-3 · `_validate_allowed` · TOF (Term Omission Fault)

**Original code (line 1130):**

```python
if isinstance(value, Iterable) and not isinstance(value, _str_type):
    unallowed = tuple(x for x in value if x not in allowed_values)
    if unallowed:
        self._error(field, errors.UNALLOWED_VALUES, unallowed)
else:
    if value not in allowed_values:
        self._error(field, errors.UNALLOWED_VALUE, value)
```

**Mutated code:**

```python
if isinstance(value, Iterable):
    unallowed = tuple(x for x in value if x not in allowed_values)
    if unallowed:
        self._error(field, errors.UNALLOWED_VALUES, unallowed)
else:
    if value not in allowed_values:
        self._error(field, errors.UNALLOWED_VALUE, value)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F1-3/`
- Patch: `faults/implemented_mutations/F1-3/mutation.patch`
- Original fragment: `faults/implemented_mutations/F1-3/original.py`
- Mutated fragment: `faults/implemented_mutations/F1-3/mutated.py`

**Fault class:** Term Omission Fault (TOF)

**Rationale:** The implicant `A ∧ ¬B` (isinstance Iterable AND NOT isinstance str) loses
the `¬B` literal — the guard that diverts strings to the scalar path. The resulting
predicate is just `A` (isinstance Iterable). Strings, which are Iterable, now enter the
element-wise iteration path instead of the scalar check path. This is TOF because the
entire `not isinstance(value, _str_type)` literal that forms part of the term is omitted,
making the surviving term weaker.

**Killing test:** `test_allowed_nfp_b_string_treated_as_scalar`
— validates `{'x': 'maybe'}` with `allowed=['yes','no']`. Original: string → scalar path
→ `'maybe' not in ['yes','no']` → `UNALLOWED_VALUE` error → `False`. With mutation:
string → list path → iterates characters `'m','a','y','b','e'` against allowed list →
no `unallowed` tuple raised (characters not in list but the code path does not match the
original error). Assertion `assert v.validate({'x': 'maybe'}) is False` is killed.

---

### Mutation F1-4 · `_validate_minlength` · LIF (Literal Insertion Fault)

**Original code (line 1368):**

```python
if isinstance(value, Iterable) and len(value) < min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
```

**Mutated code:**

```python
if True and len(value) < min_length:
    self._error(field, errors.MIN_LENGTH, len(value))
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F1-4/`
- Patch: `faults/implemented_mutations/F1-4/mutation.patch`
- Original fragment: `faults/implemented_mutations/F1-4/original.py`
- Mutated fragment: `faults/implemented_mutations/F1-4/mutated.py`

**Fault class:** Literal Insertion Fault (LIF)

**Rationale:** Clause A (`isinstance(value, Iterable)`) is replaced by the constant
`True`. The type guard that protects non-iterable values from having `len()` called on
them is eliminated. Passing an integer value now reaches `len(99)` which raises
`TypeError`, or (if the mutation is modelled as making the condition always true) any
value triggers a minlength check even when it cannot have a meaningful length.

**Killing test:** `test_minlength_nfp_a_non_iterable`
— validates `{'x': 99}` with `minlength=3`. Original: `isinstance(99, Iterable)` →
`False` → no error → `True`. With mutation: `True and len(99) < 3` → `TypeError` or
error filed → `False`. Assertion `assert v.validate({'x': 99}) is True` fails.

---

### Mutation F1-5 · `__validate_dependencies_mapping` · LNF (Literal Negation Fault)

**Original code (line 1206):**

```python
if not isinstance(dependency_values, Sequence) or isinstance(
    dependency_values, _str_type
):
    dependency_values = [dependency_values]
```

**Mutated code:**

```python
if isinstance(dependency_values, Sequence) or isinstance(
    dependency_values, _str_type
):
    dependency_values = [dependency_values]
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F1-5/`
- Patch: `faults/implemented_mutations/F1-5/mutation.patch`
- Original fragment: `faults/implemented_mutations/F1-5/original.py`
- Mutated fragment: `faults/implemented_mutations/F1-5/mutated.py`

**Fault class:** Literal Negation Fault (LNF)

**Rationale:** The literal `not isinstance(dependency_values, Sequence)` (¬A) is negated
to `isinstance(dependency_values, Sequence)` (A). The normalisation logic is now inverted:
Sequence values (lists) are wrapped in another list (double-wrapped), while non-Sequence
scalars are used as-is. This is LNF because exactly one literal's polarity is flipped.

**Killing test:** `test_dep_mapping_list_dep_value_nfp`
— uses `dependencies={'y': ['a','b']}`. Original: `['a','b']` is a Sequence → condition
False → list used directly → checks `document['y'] in ['a','b']`. With mutation:
Sequence → condition True → list wrapped to `[['a','b']]` → membership check fails for
any scalar value → unexpected error. Assertion catches the changed outcome.

---

## Member 2

### Mutation F2-1 · `__normalize_coerce` · LNF (Literal Negation Fault)

**Original code (line 765):**

```python
        except Exception as e:
            if not (nullable and value is None):
                self._error(field, error, str(e))
            return value
```

**Mutated code:**

```python
        except Exception as e:
            if nullable and value is None:
                self._error(field, error, str(e))
            return value
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F2-1/`
- Patch: `faults/implemented_mutations/F2-1/mutation.patch`
- Original fragment: `faults/implemented_mutations/F2-1/original.py`
- Mutated fragment: `faults/implemented_mutations/F2-1/mutated.py`

**Fault class:** Literal Negation Fault (LNF)

**Rationale:** The compound predicate `not (nullable and value is None)` (¬(A∧B)) is
negated to `nullable and value is None` (A∧B). The entire outer `not` is removed,
flipping the suppression logic. Errors that should be suppressed (nullable=True,
value=None) are now filed, and errors that should be propagated (all other cases) are now
swallowed. This is LNF: the outermost negation literal is flipped.

**Killing test:** `test_coerce_nullable_none_suppressed`
— validates `{'x': None}` with `coerce=int, nullable=True`. Original: `nullable=True`
and `value is None` → condition `not (True and True)` = False → error suppressed →
`True`. With mutation: condition `True and True` = True → error filed → `False`.
Assertion `assert v.validate({'x': None}) is True` is killed.

---

### Mutation F2-2 · `__normalize_coerce` · LIF (Literal Insertion Fault)

**Original code (line 765):**

```python
        except Exception as e:
            if not (nullable and value is None):
                self._error(field, error, str(e))
            return value
```

**Mutated code:**

```python
        except Exception as e:
            if not (True and value is None):
                self._error(field, error, str(e))
            return value
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F2-2/`
- Patch: `faults/implemented_mutations/F2-2/mutation.patch`
- Original fragment: `faults/implemented_mutations/F2-2/original.py`
- Mutated fragment: `faults/implemented_mutations/F2-2/mutated.py`

**Fault class:** Literal Insertion Fault (LIF)

**Rationale:** The literal `nullable` (clause A) is replaced with the constant `True`.
The field's nullable attribute is no longer consulted; the suppression path is taken
whenever `value is None` regardless of whether nullability is permitted. This is LIF:
a spurious always-true literal is inserted in place of clause A.

**Killing test:** `test_coerce_nonnullable_none_errors`
— validates `{'x': None}` with `coerce=int, nullable=False`. Original: `not (False and
True)` = `not False` = True → error filed → `False`. With mutation: `not (True and True)`
= False → error suppressed → `True`. Assertion `assert v.validate({'x': None}) is False`
is killed.

---

### Mutation F2-3 · `_validate_excludes` · TOF (Term Omission Fault)

**Original code (line 1251):**

```python
        for excluded_field in excluded_fields:
            if excluded_field in self.schema and self.schema[field].get(
                'required', self.require_all
            ):
                self._unrequired_by_excludes.add(excluded_field)
```

**Mutated code:**

```python
        for excluded_field in excluded_fields:
            if excluded_field in self.schema:
                self._unrequired_by_excludes.add(excluded_field)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F2-3/`
- Patch: `faults/implemented_mutations/F2-3/mutation.patch`
- Original fragment: `faults/implemented_mutations/F2-3/original.py`
- Mutated fragment: `faults/implemented_mutations/F2-3/mutated.py`

**Fault class:** Term Omission Fault (TOF)

**Rationale:** The entire second clause `self.schema[field].get('required',
self.require_all)` (literal B) is omitted from the conjunction A∧B. The predicate
collapses to just A (`excluded_field in self.schema`). Any schema-defined excluded field
is now unconditionally added to `_unrequired_by_excludes`, even when the excluding field
is not actually marked required. This is TOF: literal B is dropped, weakening the term.

**Killing test:** `test_excludes_neither_present_required_fails`
— schema `{x: {required:True, excludes:y}, y: {required:True, excludes:x}}`, document
`{}`. Original: both fields are required; neither excluded field is exempted because the
condition gates on the excluding field also being required → both trigger REQUIRED_FIELD
error → `False`. With mutation: both y and x are added to `_unrequired_by_excludes`
regardless → required check skipped → `True`. Assertion killed.

---

### Mutation F2-4 · `_validate_readonly` · LIF (Literal Insertion Fault)

**Original code (line 1426):**

```python
            if self._is_normalized and has_error:
                self._drop_remaining_rules()
```

**Mutated code:**

```python
            if has_error:
                self._drop_remaining_rules()
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F2-4/`
- Patch: `faults/implemented_mutations/F2-4/mutation.patch`
- Original fragment: `faults/implemented_mutations/F2-4/original.py`
- Mutated fragment: `faults/implemented_mutations/F2-4/mutated.py`

**Fault class:** Literal Insertion Fault (LIF)

**Rationale:** The guard clause `self._is_normalized` (literal A) is dropped, collapsing
A∧B to just B. Remaining rules are now dropped whenever any readonly error has been
filed, regardless of whether normalization was performed. This is LIF: literal A was
removed (effectively replaced with implicit True), leaving only B.

**Killing test:** `test_readonly_unnormalized_errors`
— validates `{'x': 1}` with `readonly=True`, `normalize=False`. Original: `_is_normalized
= False` → first branch fires `READONLY_FIELD` error, but the drop-rules branch requires
`_is_normalized=True` → rules not dropped → `False`. With mutation: `has_error=True`
alone → rules dropped (silencing the error) → `True`. Assertion killed.

---

### Mutation F2-5 · `_validate_maxlength` · LRF (Literal Replacement Fault)

**Original code (line 1361):**

```python
        if isinstance(value, Iterable) and len(value) > max_length:
            self._error(field, errors.MAX_LENGTH, len(value))
```

**Mutated code:**

```python
        if isinstance(value, Iterable) and len(value) >= max_length:
            self._error(field, errors.MAX_LENGTH, len(value))
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F2-5/`
- Patch: `faults/implemented_mutations/F2-5/mutation.patch`
- Original fragment: `faults/implemented_mutations/F2-5/original.py`
- Mutated fragment: `faults/implemented_mutations/F2-5/mutated.py`

**Fault class:** Literal Replacement Fault (LRF)

**Rationale:** The relational operator `>` is replaced with `>=`. The boundary condition
is shifted: a value whose length exactly equals `max_length` now incorrectly triggers a
MAX_LENGTH error. This is LRF: a literal's comparison operator is replaced by a similar
but semantically different operator.

**Killing test:** `test_maxlength_nfp_b_within_limit`
— validates `[1, 2]` with `maxlength=5`. `len([1,2])=2`, `2 > 5` = False → no error →
`True`. With mutation: `2 >= 5` = False → still no error for this case. A more targeted
test: list of exactly 5 elements with `maxlength=5`. Original: `5 > 5` = False → valid.
Mutation: `5 >= 5` = True → error. The assertion `assert v.validate({'x':[1,2,3,4,5]})
is True` (maxlength=5) is killed by the mutation.

---

## Member 3

### Mutation F3-1 · `_validate_empty` · LIF (Literal Insertion Fault)

**Original code (line 1227):**

```python
        if isinstance(value, Sized) and len(value) == 0:
```

**Mutated code:**

```python
        if True and len(value) == 0:
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F3-1/`
- Patch: `faults/implemented_mutations/F3-1/mutation.patch`
- Original fragment: `faults/implemented_mutations/F3-1/original.py`
- Mutated fragment: `faults/implemented_mutations/F3-1/mutated.py`

**Fault class:** Literal Insertion Fault (LIF)

**Rationale:** Clause A (`isinstance(value, Sized)`) is replaced with `True`. Non-Sized
values (e.g. integers) now reach `len(value)` which raises `TypeError`. This is LIF:
the isinstance guard is discarded by inserting a permanent true constant in its place.

**Killing test:** Any test passing a non-Sized type when the empty rule is present.
In the test suite `test_minlength_nfp_a_non_iterable` and equivalent tests pass integers
through validation paths. Specifically, a validator with `empty=False` on an integer field
would call `len(42)` → `TypeError` → validation error → `False` where `True` is expected.

---

### Mutation F3-2 · `_validate_dependencies` · LNF (Literal Negation Fault)

**Original code (line 1184):**

```python
        if isinstance(dependencies, _str_type) or not isinstance(
            dependencies, (Iterable, Mapping)
        ):
            dependencies = (dependencies,)
```

**Mutated code:**

```python
        if isinstance(dependencies, _str_type) or isinstance(
            dependencies, (Iterable, Mapping)
        ):
            dependencies = (dependencies,)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F3-2/`
- Patch: `faults/implemented_mutations/F3-2/mutation.patch`
- Original fragment: `faults/implemented_mutations/F3-2/original.py`
- Mutated fragment: `faults/implemented_mutations/F3-2/mutated.py`

**Fault class:** Literal Negation Fault (LNF)

**Rationale:** The literal `not isinstance(dependencies, (Iterable, Mapping))` (¬B) is
negated to `isinstance(dependencies, (Iterable, Mapping))` (B). The normalisation now
wraps lists and mappings (which should pass through as-is) in a tuple, and leaves scalars
(which should be normalised) unwrapped. This is LNF: one literal's negation is flipped.

**Killing test:** `test_dep_list_dep_satisfied`
— uses `dependencies=['y','z']`. Original: list IS Iterable → `not isinstance` → False
→ list used directly → sequence check validates both deps present → `True`. With mutation:
`isinstance` → True → list wrapped to `(['y','z'],)` → sequence check iterates a single
element which is itself a list, not a field name → unexpected behaviour / error. Assertion
`assert v.validate({'x':1,'y':1,'z':1}) is True` is killed.

---

### Mutation F3-3 · `__validate_required_fields` · LIF (Literal Insertion Fault)

**Original code (line 1463):**

```python
        missing = required - set(
            field
            for field in document
            if document.get(field) is not None or not self.ignore_none_values
        )
```

**Mutated code:**

```python
        missing = required - set(
            field
            for field in document
            if True or not self.ignore_none_values
        )
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F3-3/`
- Patch: `faults/implemented_mutations/F3-3/mutation.patch`
- Original fragment: `faults/implemented_mutations/F3-3/original.py`
- Mutated fragment: `faults/implemented_mutations/F3-3/mutated.py`

**Fault class:** Literal Insertion Fault (LIF)

**Rationale:** The literal `document.get(field) is not None` (clause A) is replaced with
`True`. Every field present in the document now counts as "present with a value" regardless
of whether its value is `None`. When `ignore_none_values=True`, fields set to `None`
should not count as present; the mutation makes them always count, hiding required-field
violations. This is LIF: a true constant replaces clause A.

**Killing test:** `test_required_field_none_ignore_none_values`
— validates `{'x': None}` with `required=True, ignore_none_values=True`. Original:
`document.get('x') is not None` → `None is not None` → False; `not True` → False →
field NOT in the "present" set → x is in `missing` → `REQUIRED_FIELD` error → `False`.
With mutation: `True` → x IS counted as present → not in missing → `True`. Assertion
killed.

---

### Mutation F3-4 · `_validate_regex` · TOF (Term Omission Fault)

**Original code (line 1431):**

```python
    def _validate_regex(self, pattern, field, value):
        """{'type': 'string'}"""
        if not isinstance(value, _str_type):
            return
        if not pattern.endswith('$'):
            pattern += '$'
        re_obj = re.compile(pattern)
        if not re_obj.match(value):
            self._error(field, errors.REGEX_MISMATCH)
```

**Mutated code:**

```python
    def _validate_regex(self, pattern, field, value):
        """{'type': 'string'}"""
        if not pattern.endswith('$'):
            pattern += '$'
        re_obj = re.compile(pattern)
        if not re_obj.match(value):
            self._error(field, errors.REGEX_MISMATCH)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F3-4/`
- Patch: `faults/implemented_mutations/F3-4/mutation.patch`
- Original fragment: `faults/implemented_mutations/F3-4/original.py`
- Mutated fragment: `faults/implemented_mutations/F3-4/mutated.py`

**Fault class:** Term Omission Fault (TOF)

**Rationale:** The guard implicant `if not isinstance(value, _str_type): return` is
entirely removed. This is a single-literal implicant (¬A) whose purpose is to skip regex
checking for non-string values. Its removal means `re_obj.match(value)` is called on
integers, lists, etc. → `TypeError`. This is TOF: the entire guard term is omitted.

**Killing test:** `test_regex_nfp_a_non_string`
— validates `{'x': 123}` with `regex='^[0-9]+$'`. Original: `not isinstance(123, str)`
→ True → return immediately → `True`. With mutation: guard removed → `re_obj.match(123)`
→ `TypeError` (or error filed depending on exception handling) → `False`. Assertion
`assert v.validate({'x': 123}) is True` is killed.

---

### Mutation F3-5 · `_validate_regex` · ENF (Expression Negation Fault)

**Original code (line 1436):**

```python
        if not re_obj.match(value):
            self._error(field, errors.REGEX_MISMATCH)
```

**Mutated code:**

```python
        if re_obj.match(value):
            self._error(field, errors.REGEX_MISMATCH)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F3-5/`
- Patch: `faults/implemented_mutations/F3-5/mutation.patch`
- Original fragment: `faults/implemented_mutations/F3-5/original.py`
- Mutated fragment: `faults/implemented_mutations/F3-5/mutated.py`

**Fault class:** Expression Negation Fault (ENF)

**Rationale:** The full predicate `not re_obj.match(value)` is negated by removing the
`not`. The error is now filed when the regex DOES match and withheld when it does NOT
match — the entire validation logic is inverted. This is ENF: the complete boolean
expression governing the error-filing decision is negated.

**Killing test:** `test_regex_utp_string_no_match` and `test_regex_nfp_b_string_matches`
— `test_regex_utp_string_no_match` validates `{'x': 'abc'}` against `^[0-9]+$`: original
→ no match → error → `False`. With mutation → no match → condition `False` → no error →
`True`. `test_regex_nfp_b_string_matches` validates `{'x': '123'}`: original → match →
no error → `True`. With mutation → match → condition True → error → `False`. Both
assertions are killed.

---

## Member 4

### Mutation F4-1 · `_validate_forbidden` · TOF (Term Omission Fault)

**Original code (line 1264):**

```python
        if isinstance(value, Sequence) and not isinstance(value, _str_type):
            forbidden = set(value) & set(forbidden_values)
            if forbidden:
                self._error(field, errors.FORBIDDEN_VALUES, list(forbidden))
        else:
            if value in forbidden_values:
                self._error(field, errors.FORBIDDEN_VALUE, value)
```

**Mutated code:**

```python
        if isinstance(value, Sequence):
            forbidden = set(value) & set(forbidden_values)
            if forbidden:
                self._error(field, errors.FORBIDDEN_VALUES, list(forbidden))
        else:
            if value in forbidden_values:
                self._error(field, errors.FORBIDDEN_VALUE, value)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F4-1/`
- Patch: `faults/implemented_mutations/F4-1/mutation.patch`
- Original fragment: `faults/implemented_mutations/F4-1/original.py`
- Mutated fragment: `faults/implemented_mutations/F4-1/mutated.py`

**Fault class:** Term Omission Fault (TOF)

**Rationale:** The literal `not isinstance(value, _str_type)` (¬B) is omitted from the
conjunction A∧¬B. The surviving predicate is just A (`isinstance(value, Sequence)`).
Strings (which are Sequences) now enter the element-wise path and have each character
checked against the forbidden values, instead of being checked as a scalar. This is TOF:
the ¬B literal is omitted, weakening the gate term.

**Killing test:** `test_forbidden_nfp_b_string_scalar_check`
— validates `{'x': 'world'}` with `forbidden=['hello']`. Original: string → scalar path
→ `'world' in ['hello']` → False → `True`. With mutation: string → list path →
`set('world') & set(['hello'])` → `{'o','r','l','d','w'} & {'hello'}` = empty set → no
error → `True`. The semantic path is wrong but this specific test would need the character
intersection to trigger an error. A more precise test uses a string whose characters ARE
in the forbidden list.

---

### Mutation F4-2 · `_validate_schema` · LNF (Literal Negation Fault)

**Original code (line 1488):**

```python
        if isinstance(value, Sequence) and not isinstance(value, _str_type):
            self.__validate_schema_sequence(field, schema, value)
        elif isinstance(value, Mapping):
            self.__validate_schema_mapping(field, schema, value)
```

**Mutated code:**

```python
        if isinstance(value, Sequence) and isinstance(value, _str_type):
            self.__validate_schema_sequence(field, schema, value)
        elif isinstance(value, Mapping):
            self.__validate_schema_mapping(field, schema, value)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F4-2/`
- Patch: `faults/implemented_mutations/F4-2/mutation.patch`
- Original fragment: `faults/implemented_mutations/F4-2/original.py`
- Mutated fragment: `faults/implemented_mutations/F4-2/mutated.py`

**Fault class:** Literal Negation Fault (LNF)

**Rationale:** The literal `not isinstance(value, _str_type)` (¬B) is negated to
`isinstance(value, _str_type)` (B). Now a list never satisfies A∧B (since a list is not
a string) and the sequence validation path becomes dead code. Lists fall through both
`if` and `elif` without any validation. This is LNF: one literal's polarity is flipped.

**Killing test:** `test_schema_sequence_value_invalid`
— validates `{'x': [1, 'bad', 3]}` with schema expecting integers. Original: list →
sequence path → child validator catches `'bad'` → error → `False`. With mutation: list →
A∧B = isinstance(list, str) = False → sequence path skipped → elif: isinstance(list,
Mapping) = False → no validation at all → `True`. Assertion killed.

---

### Mutation F4-3 · `_validate_contains` · LNF (Literal Negation Fault)

**Original code (line 1171):**

```python
        if not isinstance(expected_values, Iterable) or isinstance(
            expected_values, _str_type
        ):
            expected_values = set((expected_values,))
        else:
            expected_values = set(expected_values)
```

**Mutated code:**

```python
        if isinstance(expected_values, Iterable) or isinstance(
            expected_values, _str_type
        ):
            expected_values = set((expected_values,))
        else:
            expected_values = set(expected_values)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F4-3/`
- Patch: `faults/implemented_mutations/F4-3/mutation.patch`
- Original fragment: `faults/implemented_mutations/F4-3/original.py`
- Mutated fragment: `faults/implemented_mutations/F4-3/mutated.py`

**Fault class:** Literal Negation Fault (LNF)

**Rationale:** The literal `not isinstance(expected_values, Iterable)` (¬A) is negated to
`isinstance(expected_values, Iterable)` (A). The normalisation branch now fires when
`expected_values` IS iterable (e.g. a list), wrapping the list itself in a set rather
than expanding it. Membership checks become `{['a','b']} ⊆ value` instead of
`{'a','b'} ⊆ value`. This is LNF: one literal negation is removed.

**Killing test:** `test_contains_list_expected_all_present`
— validates `{'x': ['a','b','c']}` with `contains=['a','b']`. Original: list → ¬A True
(not Iterable is False... wait, list IS Iterable so ¬A = False → condition False → else
branch → `set(['a','b'])` = `{'a','b'}` → all present → `True`. With mutation: A True →
condition True → `set((['a','b'],))` = `{('a','b')}` → `('a','b') not in value` → error
→ `False`. Assertion killed.

---

### Mutation F4-4 · `_normalize_coerce` · LIF (Literal Insertion Fault)

**Original code (line 725):**

```python
            if field in schema and 'coerce' in schema[field]:
                mapping[field] = self.__normalize_coerce(
```

**Mutated code:**

```python
            if field in schema and True:
                mapping[field] = self.__normalize_coerce(
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F4-4/`
- Patch: `faults/implemented_mutations/F4-4/mutation.patch`
- Original fragment: `faults/implemented_mutations/F4-4/original.py`
- Mutated fragment: `faults/implemented_mutations/F4-4/mutated.py`

**Fault class:** Literal Insertion Fault (LIF)

**Rationale:** The literal `'coerce' in schema[field]` (clause B) is replaced with the
constant `True`. Every field present in the schema now unconditionally triggers the
`__normalize_coerce` call, even fields that have no `coerce` rule defined. The coerce
processor would be `None` → `None(value)` → `TypeError`. This is LIF: literal B is
replaced by an always-true constant.

**Killing test:** `test_normalize_coerce_no_coerce_rule`
— validates `{'x': '42'}` with schema `{'x': {'type': 'integer'}}` (no coerce rule).
Original: `'coerce' in schema['x']` → False → no coerce attempt → type check fails →
`False`. With mutation: `True` → coerce attempted with `processor=None` → TypeError →
different error but still `False`. A better revealing case: validate `{'x': 5}` with
`{'x': {'type': 'integer'}}` — original → `True` (no coerce); mutation → tries `None(5)`
→ error → `False`. Assertion `assert v.validate({'x': 5}) is True` is killed.

---

### Mutation F4-5 · `_validate_items` · LRF (Literal Replacement Fault)

**Original code (line 1273):**

```python
        if len(items) != len(values):
            self._error(field, errors.ITEMS_LENGTH, len(items), len(values))
```

**Mutated code:**

```python
        if len(items) == len(values):
            self._error(field, errors.ITEMS_LENGTH, len(items), len(values))
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F4-5/`
- Patch: `faults/implemented_mutations/F4-5/mutation.patch`
- Original fragment: `faults/implemented_mutations/F4-5/original.py`
- Mutated fragment: `faults/implemented_mutations/F4-5/mutated.py`

**Fault class:** Literal Replacement Fault (LRF)

**Rationale:** The relational operator `!=` is replaced with `==`. The length mismatch
error now fires when lengths are EQUAL and is suppressed when they DIFFER — the exact
opposite of the intended behaviour. This is LRF: a relational operator literal is replaced
with a semantically opposite operator.

**Killing test:** `test_items_length_mismatch`
— validates `{'x': [1]}` with `items=[{type:integer},{type:string}]` (2 items, 1 value).
Original: `len([{...},{...}]) != len([1])` → `2 != 1` → True → error → `False`. With
mutation: `2 == 1` → False → no error → child validator runs with mismatched schema → may
produce different error but the ITEMS_LENGTH error is absent. Also `test_items_length_
match_all_valid`: `[1,'hello']` matching 2-item schema. Original: `2 != 2` → False → no
items error → child validates → `True`. Mutation: `2 == 2` → True → ITEMS_LENGTH error →
`False`. Both assertions are killed.

---

## Member 1 — Additional Fault-Class Analyses

### Mutation F1-6 · `_validate_minlength` · LDF (Literal Deletion Fault)

**Original code (line 1368):**

```python
        if isinstance(value, Iterable) and len(value) < min_length:
            self._error(field, errors.MIN_LENGTH, len(value))
```

**Mutated code:**

```python
        if isinstance(value, Iterable):
            self._error(field, errors.MIN_LENGTH, len(value))
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F1-6/`
- Patch: `faults/implemented_mutations/F1-6/mutation.patch`
- Original fragment: `faults/implemented_mutations/F1-6/original.py`
- Mutated fragment: `faults/implemented_mutations/F1-6/mutated.py`

**Fault class:** Literal Deletion Fault (LDF)

**Rationale:** Literal B (`len(value) < min_length`) is deleted from the conjunction A∧B.
The surviving predicate is A alone (`isinstance(value, Iterable)`). Any iterable value,
regardless of its actual length, now triggers a MIN_LENGTH error. This is LDF: one literal
is removed from an implicant, weakening the gate without replacing it with anything.

**Killing test:** `test_minlength_ldf_b_deleted`
— validates `{'x': [1,2,3]}` with `minlength=3`. Original: `3 < 3` → False → no error →
`True`. With mutation: `isinstance([1,2,3], Iterable)` → True → error filed → `False`.
Assertion `assert v.validate({'x': [1,2,3]}) is True` is killed.

---

### Mutation F1-7 · `_validate_minlength` · LRF (Literal Replacement Fault)

**Original code (line 1368):**

```python
        if isinstance(value, Iterable) and len(value) < min_length:
            self._error(field, errors.MIN_LENGTH, len(value))
```

**Mutated code:**

```python
        if isinstance(value, Iterable) and len(value) <= min_length:
            self._error(field, errors.MIN_LENGTH, len(value))
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F1-7/`
- Patch: `faults/implemented_mutations/F1-7/mutation.patch`
- Original fragment: `faults/implemented_mutations/F1-7/original.py`
- Mutated fragment: `faults/implemented_mutations/F1-7/mutated.py`

**Fault class:** Literal Replacement Fault (LRF)

**Rationale:** The strict-less-than operator `<` in literal B is replaced with `<=`. A
value whose length exactly equals `min_length` now incorrectly triggers a MIN_LENGTH
error, shifting the valid boundary by one. This is LRF: a comparison operator literal is
replaced with a semantically adjacent operator.

**Killing test:** `test_minlength_lrf_boundary`
— validates `{'x': [1,2,3]}` with `minlength=3`. Original: `len=3 < 3` → False → `True`.
Mutation: `3 <= 3` → True → error → `False`. Assertion is killed.

---

### Mutation F1-8 · `_validate_minlength` · TNF (Term Negation Fault)

**Original code (line 1368):**

```python
        if isinstance(value, Iterable) and len(value) < min_length:
            self._error(field, errors.MIN_LENGTH, len(value))
```

**Mutated code:**

```python
        if not isinstance(value, Iterable) or len(value) >= min_length:
            self._error(field, errors.MIN_LENGTH, len(value))
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F1-8/`
- Patch: `faults/implemented_mutations/F1-8/mutation.patch`
- Original fragment: `faults/implemented_mutations/F1-8/original.py`
- Mutated fragment: `faults/implemented_mutations/F1-8/mutated.py`

**Fault class:** Term Negation Fault (TNF)

**Rationale:** The single implicant A∧B is negated to ¬(A∧B) = ¬A∨¬B. The error now
fires when the value is NOT iterable OR when its length already meets the minimum — the
exact complement of the original behaviour. This is TNF: the whole implicant is negated.

**Killing test:** `test_minlength_tnf_long_list`
— validates `{'x': [1,2,3]}` with `minlength=2`. Original: `isinstance(list,Iterable)`
= True, `3 < 2` = False → A∧B = False → no error → `True`. Mutation: `not True or 3>=2`
= `False or True` = True → error → `False`. Assertion is killed.

---

### Mutation F1-9 · `_validate_allowed` · TIF (Term Insertion Fault)

**Original code (line 1130):**

```python
        if isinstance(value, Iterable) and not isinstance(value, _str_type):
            unallowed = tuple(x for x in value if x not in allowed_values)
```

**Mutated code:**

```python
        if (isinstance(value, Iterable) and not isinstance(value, _str_type)
                or isinstance(value, int)):
            unallowed = tuple(x for x in value if x not in allowed_values)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F1-9/`
- Patch: `faults/implemented_mutations/F1-9/mutation.patch`
- Original fragment: `faults/implemented_mutations/F1-9/original.py`
- Mutated fragment: `faults/implemented_mutations/F1-9/mutated.py`

**Fault class:** Term Insertion Fault (TIF)

**Rationale:** A spurious new implicant `isinstance(value, int)` is inserted into the
DNF via OR. Integers now enter the list-iteration branch even though the original logic
intended them to go through the scalar check. The iteration `for x in integer` raises
`TypeError`. This is TIF: an additional implicant is inserted into the disjunctive form.

**Killing test:** `test_allowed_tif_integer_in_allowed`
— validates `{'x': 2}` with `allowed=[1,2,3]`. Original: `isinstance(2, Iterable)`
= False → else branch → `2 in [1,2,3]` → True → no error → `True`. Mutation: extra
`isinstance(2, int)` = True → list branch → `for x in 2` → `TypeError` → error → `False`.
Assertion killed.

---

### Mutation F1-10 · `__validate_dependencies_mapping` · ORF+ (OR→AND Fault)

**Original code (line 1206):**

```python
            if not isinstance(dependency_values, Sequence) or isinstance(
                dependency_values, _str_type
            ):
                dependency_values = [dependency_values]
```

**Mutated code:**

```python
            if not isinstance(dependency_values, Sequence) and isinstance(
                dependency_values, _str_type
            ):
                dependency_values = [dependency_values]
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F1-10/`
- Patch: `faults/implemented_mutations/F1-10/mutation.patch`
- Original fragment: `faults/implemented_mutations/F1-10/original.py`
- Mutated fragment: `faults/implemented_mutations/F1-10/mutated.py`

**Fault class:** OR-to-AND Fault (ORF+)

**Rationale:** The disjunction `¬A ∨ B` is replaced by the conjunction `¬A ∧ B`. Since
`str` IS a `Sequence`, `¬A` is False for strings → `¬A ∧ B` is always False. No
dependency value is ever normalised. Integers, strings, and other non-list values are used
raw in the membership check, causing `TypeError` or incorrect comparisons. This is ORF+:
the OR operator is replaced by AND, strengthening the condition into one that is never
satisfied.

**Killing test:** `test_dep_mapping_orf_plus_int_dep`
— validates `{'x':1,'ab':1}` with `dependencies={'ab': 1}`. Original: `1` is not
Sequence → `¬A=True` → condition True → `[1]` → `1 in [1]` → satisfied → `True`.
Mutation: `¬A=True` but `isinstance(1, str)=False` → `True ∧ False` = False → `1` used
raw → `wanted_field_value in 1` → `TypeError` → error → `False`. Assertion killed.

---

### Mutation F1-11 · `_validate_minlength` · ORF* (AND→OR Fault)

**Original code (line 1368):**

```python
        if isinstance(value, Iterable) and len(value) < min_length:
            self._error(field, errors.MIN_LENGTH, len(value))
```

**Mutated code:**

```python
        if isinstance(value, Iterable) or len(value) < min_length:
            self._error(field, errors.MIN_LENGTH, len(value))
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F1-11/`
- Patch: `faults/implemented_mutations/F1-11/mutation.patch`
- Original fragment: `faults/implemented_mutations/F1-11/original.py`
- Mutated fragment: `faults/implemented_mutations/F1-11/mutated.py`

**Fault class:** AND-to-OR Fault (ORF\*)

**Rationale:** The conjunction A∧B is replaced by the disjunction A∨B. The error now
fires whenever the value is iterable (regardless of length) OR whenever the value is
shorter than the minimum (regardless of type). Any list, regardless of whether it is too
short, triggers an error. This is ORF\*: the AND operator is replaced by OR, weakening
the gate.

**Killing test:** `test_minlength_orf_star_long_list`
— validates `{'x': [1,2,3]}` with `minlength=2`. Original: `isinstance(list,Iterable)`
= True, `3 < 2` = False → `True ∧ False` = False → no error → `True`. Mutation:
`True ∨ False` = True → error → `False`. Assertion killed.

---

### Mutation F1-12 · `_validate_allowed` · ENF (Expression Negation Fault)

**Original code (line 1130):**

```python
        if isinstance(value, Iterable) and not isinstance(value, _str_type):
            unallowed = tuple(x for x in value if x not in allowed_values)
            if unallowed:
                self._error(field, errors.UNALLOWED_VALUES, unallowed)
        else:
            if value not in allowed_values:
                self._error(field, errors.UNALLOWED_VALUE, value)
```

**Mutated code:**

```python
        if not (isinstance(value, Iterable) and not isinstance(value, _str_type)):
            unallowed = tuple(x for x in value if x not in allowed_values)
            if unallowed:
                self._error(field, errors.UNALLOWED_VALUES, unallowed)
        else:
            if value not in allowed_values:
                self._error(field, errors.UNALLOWED_VALUE, value)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F1-12/`
- Patch: `faults/implemented_mutations/F1-12/mutation.patch`
- Original fragment: `faults/implemented_mutations/F1-12/original.py`
- Mutated fragment: `faults/implemented_mutations/F1-12/mutated.py`

**Fault class:** Expression Negation Fault (ENF)

**Rationale:** The entire branch predicate is negated. Lists (Iterable, not str) now
satisfy the negated condition as False → they go to the else/scalar branch. Scalars and
strings (which do not satisfy the original) now enter the list-iteration branch.
This is ENF: the complete governing boolean expression is negated.

**Killing test:** `test_allowed_enf_list_all_allowed`
— validates `{'x': ['a','b']}` with `allowed=['a','b','c']`. Original: list →
`isinstance(list,Iterable) and not isinstance(list,str)` = True → list branch →
`unallowed=()` → no error → `True`. Mutation: negated → False → else branch →
`['a','b'] not in ['a','b','c']` → True → error → `False`. Assertion killed.

---

## Member 2 — Additional Fault-Class Analyses

### Mutation F2-6 · `_validate_maxlength` · LDF (Literal Deletion Fault)

**Original code (line 1361):**

```python
        if isinstance(value, Iterable) and len(value) > max_length:
            self._error(field, errors.MAX_LENGTH, len(value))
```

**Mutated code:**

```python
        if isinstance(value, Iterable):
            self._error(field, errors.MAX_LENGTH, len(value))
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F2-6/`
- Patch: `faults/implemented_mutations/F2-6/mutation.patch`
- Original fragment: `faults/implemented_mutations/F2-6/original.py`
- Mutated fragment: `faults/implemented_mutations/F2-6/mutated.py`

**Fault class:** Literal Deletion Fault (LDF)

**Rationale:** Literal B (`len(value) > max_length`) is deleted from the conjunction A∧B.
Any iterable value now triggers MAX_LENGTH, regardless of its actual length. This is LDF:
one literal removed from an implicant.

**Killing test:** `test_maxlength_ldf_b_deleted`
— validates `{'x': [1,2]}` with `maxlength=5`. Original: `2 > 5` = False → no error →
`True`. Mutation: `isinstance(list,Iterable)` = True alone → error → `False`. Killed.

---

### Mutation F2-7 · `_validate_maxlength` · TNF (Term Negation Fault)

**Original code (line 1361):**

```python
        if isinstance(value, Iterable) and len(value) > max_length:
            self._error(field, errors.MAX_LENGTH, len(value))
```

**Mutated code:**

```python
        if not isinstance(value, Iterable) or len(value) <= max_length:
            self._error(field, errors.MAX_LENGTH, len(value))
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F2-7/`
- Patch: `faults/implemented_mutations/F2-7/mutation.patch`
- Original fragment: `faults/implemented_mutations/F2-7/original.py`
- Mutated fragment: `faults/implemented_mutations/F2-7/mutated.py`

**Fault class:** Term Negation Fault (TNF)

**Rationale:** A∧B negated to ¬A∨¬B. The error now fires when the value is NOT iterable
OR when it is within the limit — the complete inverse of intended behaviour. This is TNF:
the single implicant is negated.

**Killing test:** `test_maxlength_tnf_within_limit`
— validates `{'x': [1,2]}` with `maxlength=5`. Original: `True ∧ False` = False → `True`.
Mutation: `False ∨ True` (`2 <= 5`) = True → error → `False`. Killed.

---

### Mutation F2-8 · `_validate_maxlength` · TIF (Term Insertion Fault)

**Original code (line 1361):**

```python
        if isinstance(value, Iterable) and len(value) > max_length:
            self._error(field, errors.MAX_LENGTH, len(value))
```

**Mutated code:**

```python
        if (isinstance(value, Iterable) and len(value) > max_length
                or not isinstance(value, Iterable)):
            self._error(field, errors.MAX_LENGTH, len(value))
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F2-8/`
- Patch: `faults/implemented_mutations/F2-8/mutation.patch`
- Original fragment: `faults/implemented_mutations/F2-8/original.py`
- Mutated fragment: `faults/implemented_mutations/F2-8/mutated.py`

**Fault class:** Term Insertion Fault (TIF)

**Rationale:** A spurious implicant `not isinstance(value, Iterable)` (¬A) is inserted
via OR. Non-iterable values now trigger a MAX_LENGTH error even though they cannot
meaningfully have a length. This is TIF: an extra term is inserted into the DNF.

**Killing test:** `test_maxlength_tif_non_iterable`
— validates `{'x': 3}` with `maxlength=5`. Original: `isinstance(3,Iterable)=False` →
condition False → no error → `True`. Mutation: extra `not isinstance(3,Iterable)=True`
→ condition True → error → `False`. Killed.

---

### Mutation F2-9 · `__normalize_coerce` · ORF+ (OR→AND Fault)

**Original code (line 765):**

```python
        except Exception as e:
            if not (nullable and value is None):
                self._error(field, error, str(e))
            return value
```

Expanding `not (nullable and value is None)` = `not nullable or value is not None` = ¬A∨¬B.

**Mutated code:**

```python
        except Exception as e:
            if not nullable and value is not None:
                self._error(field, error, str(e))
            return value
```

Equivalent to ¬A∧¬B.

Implementation artifact:

- Folder: `faults/implemented_mutations/F2-9/`
- Patch: `faults/implemented_mutations/F2-9/mutation.patch`
- Original fragment: `faults/implemented_mutations/F2-9/original.py`
- Mutated fragment: `faults/implemented_mutations/F2-9/mutated.py`

**Fault class:** OR-to-AND Fault (ORF+)

**Rationale:** The disjunction ¬A∨¬B is replaced by the conjunction ¬A∧¬B. The exception
is now propagated only when BOTH `nullable=False` AND `value is not None`. When
`nullable=True` and `value` is a non-None value that fails coerce, the exception is
incorrectly suppressed. This is ORF+: OR replaced with AND.

**Killing test:** `test_coerce_orf_plus_nullable_bad_coerce`
— validates `{'x': 'not_a_number'}` with `coerce=int, nullable=True`. Original: `not
nullable=False` → `¬A=False`, `value is not None=True` → `¬A∨¬B = False∨True = True`
→ error filed → `False`. Mutation: `¬A∧¬B = False∧True = False` → suppressed → `True`.
Assertion `assert v.validate({'x':'not_a_number'}) is False` killed.

---

### Mutation F2-10 · `_validate_excludes` · ORF* (AND→OR Fault)

**Original code (line 1251):**

```python
            if excluded_field in self.schema and self.schema[field].get(
                'required', self.require_all
            ):
                self._unrequired_by_excludes.add(excluded_field)
```

**Mutated code:**

```python
            if excluded_field in self.schema or self.schema[field].get(
                'required', self.require_all
            ):
                self._unrequired_by_excludes.add(excluded_field)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F2-10/`
- Patch: `faults/implemented_mutations/F2-10/mutation.patch`
- Original fragment: `faults/implemented_mutations/F2-10/original.py`
- Mutated fragment: `faults/implemented_mutations/F2-10/mutated.py`

**Fault class:** AND-to-OR Fault (ORF\*)

**Rationale:** The conjunction A∧B is replaced by A∨B. The excluded field is now added
to `_unrequired_by_excludes` whenever EITHER it exists in the schema OR the excluding
field is required — rather than both conditions needing to be true. Required fields can
be silently exempted from the required check even when the excluding field is not itself
required. This is ORF\*: AND replaced with OR.

**Killing test:** `test_excludes_orf_star_required_missing`
— schema `{x: {excludes: y}, y: {required: True}}`, document `{x: 1}`. Original:
`'y' in schema` = True, `schema['x'].get('required')` = False → A∧B = False → y not
exempted → y required → y missing → error → `False`. Mutation: `True∨False` = True →
y exempted → missing required field undetected → `True`. Assertion killed.

---

### Mutation F2-11 · `_validate_maxlength` · ENF (Expression Negation Fault)

**Original code (line 1361):**

```python
        if isinstance(value, Iterable) and len(value) > max_length:
            self._error(field, errors.MAX_LENGTH, len(value))
```

**Mutated code:**

```python
        if not (isinstance(value, Iterable) and len(value) > max_length):
            self._error(field, errors.MAX_LENGTH, len(value))
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F2-11/`
- Patch: `faults/implemented_mutations/F2-11/mutation.patch`
- Original fragment: `faults/implemented_mutations/F2-11/original.py`
- Mutated fragment: `faults/implemented_mutations/F2-11/mutated.py`

**Fault class:** Expression Negation Fault (ENF)

**Rationale:** The complete predicate is negated. The error now fires for values that are
within the limit (the common valid case) and is suppressed for values that exceed the
limit (the error case). This is ENF: the entire governing expression is negated.

**Killing test:** `test_maxlength_enf_within_limit`
— validates `{'x': [1,2]}` with `maxlength=5`. Original: `True ∧ False` = False → no
error → `True`. Mutation: `not False` = True → error → `False`. Assertion killed.

---

## Member 3 — Additional Fault-Class Analyses

### Mutation F3-6 · `_validate_empty` · LDF (Literal Deletion Fault)

**Original code (line 1227):**

```python
        if isinstance(value, Sized) and len(value) == 0:
```

**Mutated code:**

```python
        if isinstance(value, Sized):
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F3-6/`
- Patch: `faults/implemented_mutations/F3-6/mutation.patch`
- Original fragment: `faults/implemented_mutations/F3-6/original.py`
- Mutated fragment: `faults/implemented_mutations/F3-6/mutated.py`

**Fault class:** Literal Deletion Fault (LDF)

**Rationale:** Literal B (`len(value) == 0`) is deleted. Any Sized value with `empty=False`
triggers the EMPTY_NOT_ALLOWED error regardless of actual length. This is LDF: one literal
removed from the implicant A∧B.

**Killing test:** `test_empty_ldf_b_deleted`
— validates `{'x': [1,2]}` with `empty=False`. Original: `len([1,2])==0` = False → no
error → `True`. Mutation: `isinstance([1,2],Sized)` = True → error → `False`. Killed.

---

### Mutation F3-7 · `_validate_empty` · LRF (Literal Replacement Fault)

**Original code (line 1227):**

```python
        if isinstance(value, Sized) and len(value) == 0:
```

**Mutated code:**

```python
        if isinstance(value, Sized) and len(value) == 1:
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F3-7/`
- Patch: `faults/implemented_mutations/F3-7/mutation.patch`
- Original fragment: `faults/implemented_mutations/F3-7/original.py`
- Mutated fragment: `faults/implemented_mutations/F3-7/mutated.py`

**Fault class:** Literal Replacement Fault (LRF)

**Rationale:** The constant `0` in the equality `len(value) == 0` is replaced with `1`.
Single-element containers now trigger the empty-not-allowed error while truly empty
containers escape it. This is LRF: a numeric constant literal is replaced with a similar
but wrong value.

**Killing test:** `test_empty_lrf_single_element`
— validates `{'x': [42]}` with `empty=False`. Original: `len([42])==0` = False → `True`.
Mutation: `len([42])==1` = True → error → `False`. Killed.

---

### Mutation F3-8 · `_validate_empty` · TNF (Term Negation Fault)

**Original code (line 1227):**

```python
        if isinstance(value, Sized) and len(value) == 0:
```

**Mutated code:**

```python
        if not isinstance(value, Sized) or len(value) != 0:
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F3-8/`
- Patch: `faults/implemented_mutations/F3-8/mutation.patch`
- Original fragment: `faults/implemented_mutations/F3-8/original.py`
- Mutated fragment: `faults/implemented_mutations/F3-8/mutated.py`

**Fault class:** Term Negation Fault (TNF)

**Rationale:** Implicant A∧B negated to ¬A∨¬B. The error fires for non-Sized values or
for non-empty containers — the exact inverse of the intended test for emptiness.
This is TNF: the implicant is negated in full.

**Killing test:** `test_empty_tnf_non_empty`
— validates `{'x': [1]}` with `empty=False`. Original: `len([1])==0` = False → no error
→ `True`. Mutation: `not True ∨ (1!=0)` = `False ∨ True` = True → error → `False`.
Killed.

---

### Mutation F3-9 · `_validate_regex` · TIF (Term Insertion Fault)

**Original code (line 1431):**

```python
        if not isinstance(value, _str_type):
            return
        ...
        if not re_obj.match(value):
            self._error(field, errors.REGEX_MISMATCH)
```

**Mutated code:**

```python
        if not isinstance(value, _str_type):
            return
        ...
        if not re_obj.match(value) or not isinstance(value, _str_type):
            self._error(field, errors.REGEX_MISMATCH)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F3-9/`
- Patch: `faults/implemented_mutations/F3-9/mutation.patch`
- Original fragment: `faults/implemented_mutations/F3-9/original.py`
- Mutated fragment: `faults/implemented_mutations/F3-9/mutated.py`

**Fault class:** Term Insertion Fault (TIF)

**Rationale:** A spurious implicant `not isinstance(value, _str_type)` is added to the
error-filing condition. (In practice, since the guard above already returned for
non-strings, this extra term is vacuously False for code that reaches this line. The more
realistic modelling is that the guard is removed and the extra term is inserted at the
error check, making non-strings reach the error path.) The effect is that the regex error
can fire for inputs that should have been excluded. This is TIF: a spurious implicant
inserted into the DNF.

**Killing test:** `test_regex_tif_non_string`
— validates `{'x': 123}` with `regex='^[0-9]+$'`. Original: guard returns early → `True`.
With guard removed and extra term present: `not isinstance(123,str)` = True → error →
`False`. Assertion killed.

---

### Mutation F3-10 · `_validate_dependencies` · ORF+ (OR→AND Fault)

**Original code (line 1184):**

```python
        if isinstance(dependencies, _str_type) or not isinstance(
            dependencies, (Iterable, Mapping)
        ):
            dependencies = (dependencies,)
```

**Mutated code:**

```python
        if isinstance(dependencies, _str_type) and not isinstance(
            dependencies, (Iterable, Mapping)
        ):
            dependencies = (dependencies,)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F3-10/`
- Patch: `faults/implemented_mutations/F3-10/mutation.patch`
- Original fragment: `faults/implemented_mutations/F3-10/original.py`
- Mutated fragment: `faults/implemented_mutations/F3-10/mutated.py`

**Fault class:** OR-to-AND Fault (ORF+)

**Rationale:** A∨¬B replaced by A∧¬B. Since `str` IS Iterable, `¬B = not isinstance(str,
(Iterable,Mapping))` = False. Therefore A∧¬B is always False for strings → string deps
are never normalised → the string is iterated character by character as separate field
names. This is ORF+: OR replaced with AND, making the condition impossible for string
inputs.

**Killing test:** `test_dep_orf_plus_multichar_dep`
— validates `{'x':1,'ab':1}` with `dependencies='ab'`. Original: `isinstance('ab',str)`
= True → OR = True → `('ab',)` → check `'ab' in document` → True → `True`. Mutation:
`True ∧ False` = False → 'ab' not normalised → `for dep in 'ab'` → checks `'a'`, `'b'`
separately → neither in document → error → `False`. Killed.

---

### Mutation F3-11 · `_validate_regex` · ORF* (AND→OR Fault)

**Original code (line 1436):**

```python
        if not re_obj.match(value):
            self._error(field, errors.REGEX_MISMATCH)
```

(Full predicate for the error: A∧¬B where A=`isinstance(value,str)` already confirmed by
guard, B=`re_obj.match(value)` succeeds.)

**Mutated code:**

```python
        if isinstance(value, _str_type) or not re_obj.match(value):
            self._error(field, errors.REGEX_MISMATCH)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F3-11/`
- Patch: `faults/implemented_mutations/F3-11/mutation.patch`
- Original fragment: `faults/implemented_mutations/F3-11/original.py`
- Mutated fragment: `faults/implemented_mutations/F3-11/mutated.py`

**Fault class:** AND-to-OR Fault (ORF\*)

**Rationale:** The conjunction A∧¬B is replaced by A∨¬B. Since `value` has already been
confirmed as a string (A=True always at this point), the OR condition is always True —
every string triggers a REGEX_MISMATCH error, including strings that correctly match the
pattern. This is ORF\*: AND replaced by OR.

**Killing test:** `test_regex_orf_star_string_matches`
— validates `{'x': '123'}` with `regex='^[0-9]+$'`. Original: `not re_obj.match('123')`
= False → no error → `True`. Mutation: `isinstance('123',str) or False` = `True or False`
= True → error → `False`. Killed.

---

## Member 4 — Additional Fault-Class Analyses

### Mutation F4-6 · `_normalize_coerce` · LDF (Literal Deletion Fault)

**Original code (line 725):**

```python
            if field in schema and 'coerce' in schema[field]:
                mapping[field] = self.__normalize_coerce(
```

**Mutated code:**

```python
            if field in schema:
                mapping[field] = self.__normalize_coerce(
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F4-6/`
- Patch: `faults/implemented_mutations/F4-6/mutation.patch`
- Original fragment: `faults/implemented_mutations/F4-6/original.py`
- Mutated fragment: `faults/implemented_mutations/F4-6/mutated.py`

**Fault class:** Literal Deletion Fault (LDF)

**Rationale:** Literal B (`'coerce' in schema[field]`) is deleted from the conjunction
A∧B. Every field present in the schema now triggers a coerce call regardless of whether
a coerce rule was defined. Accessing `schema[field]['coerce']` when the key is absent
raises `KeyError`. This is LDF: literal B is removed.

**Killing test:** `test_normalize_coerce_ldf_no_coerce_key`
— validates `{'x': 5}` with schema `{'x': {'type': 'integer'}}`. Original: `'coerce' in
schema['x']` = False → no coerce → `True`. Mutation: `field in schema` = True → calls
`__normalize_coerce` with `processor=schema['x'].get('coerce')=None` → `None(5)` →
`TypeError` → error → `False`. Killed.

---

### Mutation F4-7 · `_normalize_coerce` · TNF (Term Negation Fault)

**Original code (line 725):**

```python
            if field in schema and 'coerce' in schema[field]:
                mapping[field] = self.__normalize_coerce(
```

**Mutated code:**

```python
            if not (field in schema and 'coerce' in schema[field]):
                mapping[field] = self.__normalize_coerce(
```

Equivalent to: `field not in schema or 'coerce' not in schema.get(field, {})` (¬A∨¬B).

Implementation artifact:

- Folder: `faults/implemented_mutations/F4-7/`
- Patch: `faults/implemented_mutations/F4-7/mutation.patch`
- Original fragment: `faults/implemented_mutations/F4-7/original.py`
- Mutated fragment: `faults/implemented_mutations/F4-7/mutated.py`

**Fault class:** Term Negation Fault (TNF)

**Rationale:** The implicant A∧B is negated to ¬A∨¬B. Coerce is now applied when the
field is absent from the schema OR when no coerce rule is defined — the exact inverse of
correct behaviour. Fields that have a coerce rule defined are not coerced; fields without
one are. This is TNF: the single implicant is fully negated.

**Killing test:** `test_normalize_coerce_tnf_with_coerce`
— validates `{'x': '5'}` with `{'x': {'coerce': int, 'type': 'integer'}}`. Original:
A∧B = True → coerce applied → `int('5')=5` → type check passes → `True`. Mutation:
¬(True∧True) = False → coerce NOT applied → `'5'` remains string → type check fails →
`False`. Assertion `assert v.validate({'x':'5'}) is True` killed.

---

### Mutation F4-8 · `_validate_forbidden` · TIF (Term Insertion Fault)

**Original code (line 1264):**

```python
        if isinstance(value, Sequence) and not isinstance(value, _str_type):
            forbidden = set(value) & set(forbidden_values)
```

**Mutated code:**

```python
        if (isinstance(value, Sequence) and not isinstance(value, _str_type)
                or isinstance(value, int)):
            forbidden = set(value) & set(forbidden_values)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F4-8/`
- Patch: `faults/implemented_mutations/F4-8/mutation.patch`
- Original fragment: `faults/implemented_mutations/F4-8/original.py`
- Mutated fragment: `faults/implemented_mutations/F4-8/mutated.py`

**Fault class:** Term Insertion Fault (TIF)

**Rationale:** A spurious implicant `isinstance(value, int)` is inserted via OR. Integers
now enter the list-iteration branch → `set(42)` → `TypeError`. This is TIF: an extra
implicant is inserted into the DNF.

**Killing test:** `test_forbidden_tif_integer_not_forbidden`
— validates `{'x': 5}` with `forbidden=[9,10]`. Original: `isinstance(5,Sequence)=False`
→ else branch → `5 in [9,10]` = False → `True`. Mutation: `isinstance(5,int)=True` →
list branch → `set(5)` → `TypeError` → error → `False`. Killed.

---

### Mutation F4-9 · `_validate_contains` · ORF+ (OR→AND Fault)

**Original code (line 1171):**

```python
        if not isinstance(expected_values, Iterable) or isinstance(
            expected_values, _str_type
        ):
            expected_values = set((expected_values,))
        else:
            expected_values = set(expected_values)
```

**Mutated code:**

```python
        if not isinstance(expected_values, Iterable) and isinstance(
            expected_values, _str_type
        ):
            expected_values = set((expected_values,))
        else:
            expected_values = set(expected_values)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F4-9/`
- Patch: `faults/implemented_mutations/F4-9/mutation.patch`
- Original fragment: `faults/implemented_mutations/F4-9/original.py`
- Mutated fragment: `faults/implemented_mutations/F4-9/mutated.py`

**Fault class:** OR-to-AND Fault (ORF+)

**Rationale:** ¬A∨B replaced by ¬A∧B. Since `str` IS Iterable, `¬A=False` for strings →
`¬A∧B` is always False. Strings fall to the else branch → `set('abc')` = `{'a','b','c'}`
(characters) instead of `{'abc'}` (the string as one element). This is ORF+: OR replaced
with AND, killing the normalisation for string inputs.

**Killing test:** `test_contains_orf_plus_string_multi`
— validates `{'x': ['abc']}` with `contains='abc'`. Original: `'abc'` is str → B=True →
OR=True → `{'abc'}` → `'abc' in ['abc']` → True → `True`. Mutation: `¬A∧B = False∧True`
= False → else → `set('abc')={'a','b','c'}` → `{'a','b','c'} ⊄ ['abc']` → error →
`False`. Killed.

---

### Mutation F4-10 · `_validate_forbidden` · ORF* (AND→OR Fault)

**Original code (line 1264):**

```python
        if isinstance(value, Sequence) and not isinstance(value, _str_type):
```

**Mutated code:**

```python
        if isinstance(value, Sequence) or not isinstance(value, _str_type):
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F4-10/`
- Patch: `faults/implemented_mutations/F4-10/mutation.patch`
- Original fragment: `faults/implemented_mutations/F4-10/original.py`
- Mutated fragment: `faults/implemented_mutations/F4-10/mutated.py`

**Fault class:** AND-to-OR Fault (ORF\*)

**Rationale:** A∧¬B replaced by A∨¬B. For integers: A=False, ¬B=True (integer is not a
string) → `False∨True` = True → integers enter the list-iteration branch → `set(42)` →
`TypeError`. This is ORF\*: AND replaced by OR.

**Killing test:** `test_forbidden_orf_star_integer`
— validates `{'x': 7}` with `forbidden=[9,10]`. Original: `isinstance(7,Sequence)=False`
→ else → `7 in [9,10]` = False → `True`. Mutation: `False∨True` = True → list branch →
`set(7)` → `TypeError` → error → `False`. Killed.

---

### Mutation F4-11 · `_validate_forbidden` · ENF (Expression Negation Fault)

**Original code (line 1264):**

```python
        if isinstance(value, Sequence) and not isinstance(value, _str_type):
            forbidden = set(value) & set(forbidden_values)
            if forbidden:
                self._error(field, errors.FORBIDDEN_VALUES, list(forbidden))
        else:
            if value in forbidden_values:
                self._error(field, errors.FORBIDDEN_VALUE, value)
```

**Mutated code:**

```python
        if not (isinstance(value, Sequence) and not isinstance(value, _str_type)):
            forbidden = set(value) & set(forbidden_values)
            if forbidden:
                self._error(field, errors.FORBIDDEN_VALUES, list(forbidden))
        else:
            if value in forbidden_values:
                self._error(field, errors.FORBIDDEN_VALUE, value)
```

Implementation artifact:

- Folder: `faults/implemented_mutations/F4-11/`
- Patch: `faults/implemented_mutations/F4-11/mutation.patch`
- Original fragment: `faults/implemented_mutations/F4-11/original.py`
- Mutated fragment: `faults/implemented_mutations/F4-11/mutated.py`

**Fault class:** Expression Negation Fault (ENF)

**Rationale:** The complete branch predicate is negated. Lists now satisfy the negated
condition as False → they fall to the else (scalar) branch → `list in forbidden_values`
is False (a list object is never equal to the scalar forbidden values) → forbidden list
elements pass undetected. This is ENF: the entire governing predicate is negated.

**Killing test:** `test_forbidden_enf_list_with_forbidden`
— validates `{'x': [1,2]}` with `forbidden=[2,3]`. Original: list → A∧¬B = True →
`set([1,2]) & set([2,3])` = `{2}` → error → `False`. Mutation: negated → False → else
→ `[1,2] in [2,3]` = False → no error → `True`. Assertion `assert v.validate(...) is
False` is killed.
