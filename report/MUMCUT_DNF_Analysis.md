# MUMCUT-Based Test Requirement Generation and DNF Fault Analysis for Cerberus Group C

---

## 1. Selected Functions Table

| # | Member | Function | File:Line | Predicate Form |
|---|--------|----------|-----------|----------------|
| 1 | 1 | `_validate_type` | `validator.py:1543` | `A ∧ ¬B` |
| 2 | 1 | `_validate_allowed` | `validator.py:1130` | `A ∧ ¬B` |
| 3 | 1 | `__validate_unknown_fields` | `validator.py:1066` | nested `A`, then `B` |
| 4 | 1 | `_validate_minlength` | `validator.py:1368` | `A ∧ B` |
| 5 | 1 | `__validate_dependencies_mapping` | `validator.py:1206` | `¬A ∨ B` |
| 6 | 2 | `__normalize_coerce` | `validator.py:765` | `¬(A ∧ B)` = `¬A ∨ ¬B` |
| 7 | 2 | `_validate_excludes` | `validator.py:1251` | `A ∧ B` |
| 8 | 2 | `_validate_readonly` | `validator.py:1426` | `A ∧ B` |
| 9 | 2 | `_validate_maxlength` | `validator.py:1361` | `A ∧ B` |
| 10 | 2 | `_validate_keysrules` | `validator.py:1402` | nested `A`, inner `¬B` |
| 11 | 3 | `_validate_empty` | `validator.py:1227` | `A ∧ B` |
| 12 | 3 | `_validate_dependencies` | `validator.py:1184` | `A ∨ ¬B` |
| 13 | 3 | `__validate_required_fields` | `validator.py:1465` | `A ∨ ¬B` |
| 14 | 3 | `_validate_regex` | `validator.py:1431` | `A ∧ ¬B` (across two `if`s) |
| 15 | 3 | `_validate_valuesrules` | `validator.py:1569` | nested `A`, inner `B` |
| 16 | 4 | `_validate_forbidden` | `validator.py:1264` | `A ∧ ¬B` |
| 17 | 4 | `_validate_schema` | `validator.py:1488` | `A ∧ ¬B` / `elif C` |
| 18 | 4 | `_validate_contains` | `validator.py:1171` | `¬A ∨ B` |
| 19 | 4 | `_normalize_coerce` | `validator.py:725` | `A ∧ B` |
| 20 | 4 | `_validate_items` | `validator.py:1273` | `A` / `¬B` across branches |

---

## 2. DNF Derivations

### 2.1 `_validate_type`

**Function name:** `_validate_type`

**Source predicate (line 1543):**
```python
matched = isinstance(value, type_definition.included_types) \
          and not isinstance(value, type_definition.excluded_types)
```

Let $A$ = `isinstance(value, included_types)`, $B$ = `isinstance(value, excluded_types)`.

#### Step 1 - Predicate Extraction

$$p = A \land \lnot B$$

The function sets `matched = True` only when the value belongs to the included types AND
does not belong to the excluded types. If `matched` remains False for all type candidates,
`BAD_TYPE` is raised.

#### Step 2 - DNF Conversion

The predicate is already a single conjunctive term. DNF is trivial:

$$p = A \land \lnot B$$

#### Step 3 - Terms and Literals

- **Terms (implicants):** $\{A\lnot B\}$
- **Literals:** $A$, $\lnot B$
- **Major literals:** $A$ (determines $p$ when $\lnot B = T$), $\lnot B$ (determines $p$ when $A = T$)

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

One implicant → one MUTP.

| Point | A | B | p |
|-------|---|---|---|
| MUTP-1 | T | F | T |

##### CUTPNFP requirements

For each literal, one CUTPNFP (unique true point that becomes a near-false point when the literal is flipped):

| Literal | CUTPNFP | A | B | p |
|---------|---------|---|---|---|
| A | NFP-A | F | F | F |
| ¬B | NFP-B | T | T | F |

##### MNFP requirements

Single implicant → no separate MNFP needed (CUTPNFP covers near-false requirement).

#### Step 5 - Generated Test Requirements

1. MUTP-1: value matches included_types, does not match excluded_types → `matched=True`
2. NFP-A: value does not match included_types → `matched=False`
3. NFP-B: value matches both included_types and excluded_types → `matched=False`

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_type_utp_both_clauses_true_no_error` |
| NFP-A | `test_type_nfp_clause_a_false_error` |
| NFP-B | `test_type_nfp_clause_b_true_error` |

---

### 2.2 `_validate_allowed`

**Function name:** `_validate_allowed`

**Source predicate (line 1130):**
```python
if isinstance(value, Iterable) and not isinstance(value, _str_type):
    # list path
else:
    # scalar path
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `isinstance(value, _str_type)`.

#### Step 1 - Predicate Extraction

$$p = A \land \lnot B$$

#### Step 2 - DNF Conversion

Already in minimal DNF:

$$p = A \land \lnot B$$

#### Step 3 - Terms and Literals

- **Terms:** $\{A\lnot B\}$
- **Literals:** $A$, $\lnot B$
- **Major literals:** $A$, $\lnot B$

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | p |
|-------|---|---|---|
| MUTP-1 | T | F | T |

##### CUTPNFP requirements

| Literal | Point | A | B | p |
|---------|-------|---|---|---|
| A | NFP-A | F | F | F |
| ¬B | NFP-B | T | T | F |

##### MNFP requirements

None (single implicant).

#### Step 5 - Generated Test Requirements

1. MUTP-1: list value (Iterable, not str) → list check path
2. NFP-A: integer value (not Iterable) → scalar path
3. NFP-B: string value (Iterable and str) → scalar path

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_allowed_utp_list_all_allowed` |
| NFP-A | `test_allowed_nfp_a_non_iterable_scalar_unallowed` |
| NFP-B | `test_allowed_nfp_b_string_treated_as_scalar` |

---

### 2.3 `__validate_unknown_fields`

**Function name:** `__validate_unknown_fields`

**Source predicate (line 1066):**
```python
if self.allow_unknown:              # outer: A
    if isinstance(self.allow_unknown, (Mapping, _str_type)):  # inner: B
        # sub-validate
```

Let $A$ = `bool(self.allow_unknown)` (truthy), $B$ = `isinstance(allow_unknown, (Mapping, _str_type))`.

#### Step 1 - Predicate Extraction

Outer: $p_1 = A$. When true, inner: $p_2 = B$.

The combined predicate for sub-validation is $p = A \land B$.

#### Step 2 - DNF Conversion

$$p = A \land B$$

#### Step 3 - Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | p |
|-------|---|---|---|
| MUTP-1 | T | T | T |

##### CUTPNFP requirements

| Literal | Point | A | B | p |
|---------|-------|---|---|---|
| A | NFP-A | F | T | F |
| B | NFP-B | T | F | F |

##### MNFP requirements

None (single implicant).

#### Step 5 - Generated Test Requirements

1. MUTP-1: `allow_unknown=Mapping` → sub-validates unknown field
2. NFP-A: `allow_unknown=False` → unknown field rejected
3. NFP-B: `allow_unknown=True` (not Mapping/str) → unknown accepted without sub-validation

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 (A=T,B=T) | `test_unknown_fields_allow_unknown_schema_valid` |
| NFP-A (A=F) | `test_unknown_fields_not_allowed_error` |
| NFP-B (A=T,B=F) | `test_unknown_fields_allow_unknown_true` |

---

### 2.4 `_validate_minlength`

**Function name:** `_validate_minlength`

**Source predicate (line 1368):**
```python
if isinstance(value, Iterable) and len(value) < min_length:
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `len(value) < min_length`.

#### Step 1 - Predicate Extraction

$$p = A \land B$$

#### Step 2 - DNF Conversion

$$p = A \land B$$

#### Step 3 - Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | p |
|-------|---|---|---|
| MUTP-1 | T | T | T |

##### CUTPNFP requirements

| Literal | Point | A | B | p |
|---------|-------|---|---|---|
| A | NFP-A | F | T | F |
| B | NFP-B | T | F | F |

##### MNFP requirements

None (single implicant).

#### Step 5 - Generated Test Requirements

1. MUTP-1: Iterable value with length < min → MIN_LENGTH error
2. NFP-A: non-Iterable value → no error
3. NFP-B: Iterable value with length ≥ min → no error

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_minlength_utp_list_too_short` |
| NFP-A | `test_minlength_nfp_a_non_iterable` |
| NFP-B | `test_minlength_nfp_b_list_long_enough` |

---

### 2.5 `__validate_dependencies_mapping`

**Function name:** `__validate_dependencies_mapping`

**Source predicate (line 1206):**
```python
if not isinstance(dependency_values, Sequence) or isinstance(
    dependency_values, _str_type
):
    dependency_values = [dependency_values]
```

Let $A$ = `isinstance(dependency_values, Sequence)`, $B$ = `isinstance(dependency_values, _str_type)`.

#### Step 1 - Predicate Extraction

$$p = \lnot A \lor B$$

#### Step 2 - DNF Conversion

Two implicants:

$$p = \lnot A \lor B$$

#### Step 3 - Terms and Literals

- **Terms:** $\{\lnot A\}$, $\{B\}$
- **Literals:** $\lnot A$, $B$
- **Major literals:** $\lnot A$ (unique to first term), $B$ (unique to second term)

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

Two implicants → two MUTPs.

| Point | A | B | Via implicant | p |
|-------|---|---|---------------|---|
| MUTP-¬A | F | F | ¬A | T |
| MUTP-B | T | T | B | T |

##### CUTPNFP requirements

| Implicant | Literal | NFP | A | B | p |
|-----------|---------|-----|---|---|---|
| ¬A | A (flip ¬A→A) | NFP-¬A | T | F | F |
| B | B (flip B→¬B) | NFP-B | T | F | F |

Both NFPs map to the same test point $(A=T, B=F)$: value is a non-string Sequence.

##### MNFP requirements

| For implicant | MNFP | A | B | p |
|---------------|------|---|---|---|
| ¬A | $(A=T,B=F)$ | T | F | F |
| B | $(A=T,B=F)$ | T | F | F |

#### Step 5 - Generated Test Requirements

1. MUTP-¬A: scalar (non-Sequence) dep value → normalised to list
2. MUTP-B: string dep value → normalised to list
3. NFP: list dep value → used directly (predicate false)

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-¬A | `test_dep_mapping_scalar_dep_value_satisfied` |
| MUTP-B | `test_dep_mapping_string_dep_value_satisfied` |
| NFP | `test_dep_mapping_list_dep_value_nfp` |

---

### 2.6 `__normalize_coerce`

**Function name:** `__normalize_coerce`

**Source predicate (line 765):**
```python
if not (nullable and value is None):
    self._error(field, error, str(e))
```

Let $A$ = `nullable`, $B$ = `value is None`.

#### Step 1 - Predicate Extraction

$$p = \lnot(A \land B) = \lnot A \lor \lnot B$$

#### Step 2 - DNF Conversion

$$p = \lnot A \lor \lnot B$$

Two implicants: $\lnot A$ and $\lnot B$.

#### Step 3 - Terms and Literals

- **Terms:** $\{\lnot A\}$, $\{\lnot B\}$
- **Literals:** $\lnot A$, $\lnot B$
- **Major literals:** $\lnot A$ (unique to first), $\lnot B$ (unique to second)

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | Via | p |
|-------|---|---|-----|---|
| MUTP-¬A | F | T | ¬A | T |
| MUTP-¬B | T | F | ¬B | T |

##### CUTPNFP requirements

| Implicant | Literal | NFP | A | B | p |
|-----------|---------|-----|---|---|---|
| ¬A | flip to A | NFP-¬A | T | T | F |
| ¬B | flip to B | NFP-¬B | T | T | F |

Both NFPs collapse to $(A=T, B=T)$: nullable=True, value=None → error suppressed.

##### MNFP requirements

$(A=T, B=T)$: the only false point.

#### Step 5 - Generated Test Requirements

1. MUTP-¬A: `nullable=False, value=None` → error filed
2. MUTP-¬B: `nullable=True, value≠None` → error filed
3. NFP/MNFP: `nullable=True, value=None` → error suppressed

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-¬A | `test_coerce_nonnullable_none_errors` |
| MUTP-¬B | `test_coerce_nullable_non_none_coerces` |
| NFP | `test_coerce_nullable_none_suppressed` |

---

### 2.7 `_validate_excludes`

**Function name:** `_validate_excludes`

**Source predicate (line 1251):**
```python
if excluded_field in self.schema and self.schema[field].get(
    'required', self.require_all
):
    self._unrequired_by_excludes.add(excluded_field)
```

Let $A$ = `excluded_field in self.schema`, $B$ = `self.schema[field].get('required', require_all)`.

#### Step 1 - Predicate Extraction

$$p = A \land B$$

#### Step 2 - DNF Conversion

$$p = A \land B$$

#### Step 3 - Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | p |
|-------|---|---|---|
| MUTP-1 | T | T | T |

##### CUTPNFP requirements

| Literal | Point | A | B | p |
|---------|-------|---|---|---|
| A | NFP-A | F | T | F |
| B | NFP-B | T | F | F |

##### MNFP requirements

None.

#### Step 5 - Generated Test Requirements

1. MUTP-1: excluded field in schema and excluding field required → excluded marked unrequired
2. NFP-A: excluded field not in schema → no exemption
3. NFP-B: excluding field not required → no exemption

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_excludes_required_one_present` |
| NFP-B | `test_excludes_neither_present_required_fails` |

---

### 2.8 `_validate_readonly`

**Function name:** `_validate_readonly`

**Source predicate (line 1426):**
```python
if self._is_normalized and has_error:
    self._drop_remaining_rules()
```

Let $A$ = `self._is_normalized`, $B$ = `has_error`.

#### Step 1 - Predicate Extraction

$$p = A \land B$$

#### Step 2 - DNF Conversion

$$p = A \land B$$

#### Step 3 - Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | p |
|-------|---|---|---|
| MUTP-1 | T | T | T |

##### CUTPNFP requirements

| Literal | Point | A | B | p |
|---------|-------|---|---|---|
| A | NFP-A | F | T | F |
| B | NFP-B | T | F | F |

##### MNFP requirements

None.

#### Step 5 - Generated Test Requirements

1. MUTP-1: normalized=True and has_error=True → rules dropped
2. NFP-A: normalized=False → READONLY_FIELD error (first branch), rules not dropped
3. NFP-B: normalized=True and no prior error → no drop

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| NFP-A | `test_readonly_unnormalized_errors` |
| NFP-B | `test_readonly_normalized_no_value_change` |
| MUTP-1 | `test_readonly_normalized_value_present_errors` |

---

### 2.9 `_validate_maxlength`

**Function name:** `_validate_maxlength`

**Source predicate (line 1361):**
```python
if isinstance(value, Iterable) and len(value) > max_length:
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `len(value) > max_length`.

#### Step 1 - Predicate Extraction

$$p = A \land B$$

#### Step 2 - DNF Conversion

$$p = A \land B$$

#### Step 3 - Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | p |
|-------|---|---|---|
| MUTP-1 | T | T | T |

##### CUTPNFP requirements

| Literal | Point | A | B | p |
|---------|-------|---|---|---|
| A | NFP-A | F | T | F |
| B | NFP-B | T | F | F |

##### MNFP requirements

None.

#### Step 5 - Generated Test Requirements

1. MUTP-1: Iterable value with length > max → MAX_LENGTH error
2. NFP-A: non-Iterable → no check
3. NFP-B: Iterable within limit → no error

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_maxlength_utp_list_too_long` |
| NFP-A | `test_maxlength_nfp_a_non_iterable` |
| NFP-B | `test_maxlength_nfp_b_within_limit` |

---

### 2.10 `_validate_keysrules`

**Function name:** `_validate_keysrules`

**Source predicate (line 1402):**
```python
if isinstance(value, Mapping):
    ...
    if not validator(...):
        self._error(...)
```

Let $A$ = `isinstance(value, Mapping)`, $B$ = `not validator(...)` (child validation fails).

#### Step 1 - Predicate Extraction

Outer: $p_1 = A$. Inner: $p_2 = \lnot B_{pass}$ where $B_{pass}$ = child validator returns True.

Combined error predicate: $p = A \land \lnot B_{pass}$.

#### Step 2 - DNF Conversion

$$p = A \land \lnot B_{pass}$$

#### Step 3 - Terms and Literals

- **Terms:** $\{A\lnot B_{pass}\}$
- **Literals:** $A$, $\lnot B_{pass}$
- **Major literals:** $A$, $\lnot B_{pass}$

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B_pass | p |
|-------|---|--------|---|
| MUTP-1 | T | F | T |

##### CUTPNFP requirements

| Literal | NFP | A | B_pass | p |
|---------|-----|---|--------|---|
| A | NFP-A | F | F | F |
| ¬B_pass | NFP-B | T | T | F |

##### MNFP requirements

None.

#### Step 5 - Generated Test Requirements

1. MUTP-1: Mapping value with key failing keysrules → error
2. NFP-A: non-Mapping value → keysrules skipped
3. NFP-B: Mapping value with all keys passing → no error

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_keysrules_utp_mapping_keys_invalid` |
| NFP-A | `test_keysrules_nfp_outer_not_mapping` |
| NFP-B | `test_keysrules_utp_mapping_keys_valid` |

---

### 2.11 `_validate_empty`

**Function name:** `_validate_empty`

**Source predicate (line 1227):**
```python
if isinstance(value, Sized) and len(value) == 0:
```

Let $A$ = `isinstance(value, Sized)`, $B$ = `len(value) == 0`.

#### Step 1 - Predicate Extraction

$$p = A \land B$$

#### Step 2 - DNF Conversion

$$p = A \land B$$

#### Step 3 - Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | p |
|-------|---|---|---|
| MUTP-1 | T | T | T |

##### CUTPNFP requirements

| Literal | Point | A | B | p |
|---------|-------|---|---|---|
| A | NFP-A | F | T | F |
| B | NFP-B | T | F | F |

##### MNFP requirements

None.

#### Step 5 - Generated Test Requirements

1. MUTP-1: empty Sized value with `empty=False` → EMPTY_NOT_ALLOWED error
2. NFP-A: non-Sized value → no empty check
3. NFP-B: non-empty Sized value → no error

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_empty_utp_empty_list_not_allowed` |
| NFP-B | `test_empty_nfp_b_non_empty_list` |

---

### 2.12 `_validate_dependencies`

**Function name:** `_validate_dependencies`

**Source predicate (line 1184):**
```python
if isinstance(dependencies, _str_type) or not isinstance(
    dependencies, (Iterable, Mapping)
):
    dependencies = (dependencies,)
```

Let $A$ = `isinstance(dependencies, _str_type)`, $B$ = `isinstance(dependencies, (Iterable, Mapping))`.

#### Step 1 - Predicate Extraction

$$p = A \lor \lnot B$$

#### Step 2 - DNF Conversion

$$p = A \lor \lnot B$$

Two implicants: $A$ and $\lnot B$.

#### Step 3 - Terms and Literals

- **Terms:** $\{A\}$, $\{\lnot B\}$
- **Literals:** $A$, $\lnot B$
- **Major literals:** $A$ (unique to first), $\lnot B$ (unique to second)

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | Via | p |
|-------|---|---|-----|---|
| MUTP-A | T | T | A | T |
| MUTP-¬B | F | F | ¬B | T |

##### CUTPNFP requirements

| Implicant | Literal | NFP | A | B | p |
|-----------|---------|-----|---|---|---|
| A | flip A→¬A | NFP-A | F | T | F |
| ¬B | flip ¬B→B | NFP-¬B | F | T | F |

Both NFPs collapse to $(A=F, B=T)$: list deps.

##### MNFP requirements

$(A=F, B=T)$: the only false point for this DNF.

#### Step 5 - Generated Test Requirements

1. MUTP-A: string dep → normalised
2. MUTP-¬B: scalar dep (not Iterable/Mapping) → normalised
3. NFP: list dep → used directly

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-A | `test_dep_string_dep_present` |
| NFP | `test_dep_list_dep_satisfied` |

---

### 2.13 `__validate_required_fields`

**Function name:** `__validate_required_fields`

**Source predicate (line 1463):**
```python
if document.get(field) is not None or not self.ignore_none_values
```

Let $A$ = `document.get(field) is not None`, $B$ = `self.ignore_none_values`.

#### Step 1 - Predicate Extraction

$$p = A \lor \lnot B$$

A field counts as "present" (not missing) when its value is not None OR when
`ignore_none_values` is False.

#### Step 2-— DNF Conversion

$$p = A \lor \lnot B$$

Two implicants: $A$ and $\lnot B$.

#### Step 3 - Terms and Literals

- **Terms:** $\{A\}$, $\{\lnot B\}$
- **Literals:** $A$, $\lnot B$
- **Major literals:** $A$, $\lnot B$

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | Via | p |
|-------|---|---|-----|---|
| MUTP-A | T | T | A | T |
| MUTP-¬B | F | F | ¬B | T |

##### CUTPNFP requirements

| Implicant | Literal | NFP | A | B | p |
|-----------|---------|-----|---|---|---|
| A | flip A→¬A | NFP-A | F | T | F |
| ¬B | flip ¬B→B | NFP-¬B | F | T | F |

Both collapse to $(A=F, B=T)$: `field=None, ignore_none_values=True`.

##### MNFP requirements

$(A=F, B=T)$.

#### Step 5 - Generated Test Requirements

1. MUTP-A: field has non-None value, ignore_none_values=True → field counts as present
2. MUTP-¬B: ignore_none_values=False → None-valued field counts as present
3. NFP: field=None, ignore_none_values=True → field NOT counted → required error

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-A | `test_required_field_present` |
| MUTP-¬B | `test_required_field_none_not_ignore` |
| NFP | `test_required_field_none_ignore_none_values` |

---

### 2.14 `_validate_regex`

**Function name:** `_validate_regex`

**Source predicates (lines 1431, 1436):**
```python
if not isinstance(value, _str_type):    # guard: ¬A → early return
    return
...
if not re_obj.match(value):             # error: ¬B
    self._error(field, errors.REGEX_MISMATCH)
```

Let $A$ = `isinstance(value, _str_type)`, $B$ = `re_obj.match(value)` succeeds.

#### Step 1 - Predicate Extraction

The error fires when: $A$ is True (not returned early) AND $\lnot B$ (match fails).

$$p_{err} = A \land \lnot B$$

#### Step 2 - DNF Conversion

$$p_{err} = A \land \lnot B$$

#### Step 3 - Terms and Literals

- **Terms:** $\{A\lnot B\}$
- **Literals:** $A$, $\lnot B$
- **Major literals:** $A$, $\lnot B$

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | p |
|-------|---|---|---|
| MUTP-1 | T | F | T |

##### CUTPNFP requirements

| Literal | Point | A | B | p |
|---------|-------|---|---|---|
| A | NFP-A | F | F | F |
| ¬B | NFP-B | T | T | F |

##### MNFP requirements

None.

#### Step 5 - Generated Test Requirements

1. MUTP-1: string value that does not match → REGEX_MISMATCH error
2. NFP-A: non-string value → guard returns → no error
3. NFP-B: string value that matches → no error

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_regex_utp_string_no_match` |
| NFP-A | `test_regex_nfp_a_non_string` |
| NFP-B | `test_regex_nfp_b_string_matches` |

---

### 2.15 `_validate_valuesrules`

**Function name:** `_validate_valuesrules`

**Source predicate (line 1569):**
```python
if isinstance(value, Mapping):
    validator(...)
    if validator._errors:
        self._error(...)
```

Let $A$ = `isinstance(value, Mapping)`, $B$ = `validator._errors` (child has errors).

#### Step 1 - Predicate Extraction

$$p = A \land B$$

#### Step 2 - DNF Conversion

$$p = A \land B$$

#### Step 3 - Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | p |
|-------|---|---|---|
| MUTP-1 | T | T | T |

##### CUTPNFP requirements

| Literal | Point | A | B | p |
|---------|-------|---|---|---|
| A | NFP-A | F | T | F |
| B | NFP-B | T | F | F |

##### MNFP requirements

None.

#### Step 5 - Generated Test Requirements

1. MUTP-1: Mapping with invalid value → error
2. NFP-A: non-Mapping → no check
3. NFP-B: Mapping with all valid values → no error

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_valuesrules_mapping_value_invalid` |
| NFP-A | `test_valuesrules_nfp_not_mapping` |
| NFP-B | `test_valuesrules_mapping_values_valid` |

---

### 2.16 `_validate_forbidden`

**Function name:** `_validate_forbidden`

**Source predicate (line 1264):**
```python
if isinstance(value, Sequence) and not isinstance(value, _str_type):
```

Let $A$ = `isinstance(value, Sequence)`, $B$ = `isinstance(value, _str_type)`.

#### Step 1 - Predicate Extraction

$$p = A \land \lnot B$$

#### Step 2 - DNF Conversion

$$p = A \land \lnot B$$

#### Step 3 - Terms and Literals

- **Terms:** $\{A\lnot B\}$
- **Literals:** $A$, $\lnot B$
- **Major literals:** $A$, $\lnot B$

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | p |
|-------|---|---|---|
| MUTP-1 | T | F | T |

##### CUTPNFP requirements

| Literal | Point | A | B | p |
|---------|-------|---|---|---|
| A | NFP-A | F | F | F |
| ¬B | NFP-B | T | T | F |

##### MNFP requirements

None.

#### Step 5 - Generated Test Requirements

1. MUTP-1: list value → element-wise forbidden check
2. NFP-A: scalar value (not Sequence) → scalar check
3. NFP-B: string value (Sequence and str) → scalar check

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_forbidden_utp_list_with_forbidden_element` |
| NFP-A | `test_forbidden_nfp_a_scalar_forbidden` |
| NFP-B | `test_forbidden_nfp_b_string_scalar_check` |

---

### 2.17 `_validate_schema`

**Function name:** `_validate_schema`

**Source predicate (line 1488):**
```python
if isinstance(value, Sequence) and not isinstance(value, _str_type):
    self.__validate_schema_sequence(...)
elif isinstance(value, Mapping):
    self.__validate_schema_mapping(...)
```

Let $A$ = `isinstance(value, Sequence)`, $B$ = `isinstance(value, _str_type)`, $C$ = `isinstance(value, Mapping)`.

#### Step 1 - Predicate Extraction

Branch 1 predicate: $p_1 = A \land \lnot B$
Branch 2 predicate: $p_2 = \lnot(A \land \lnot B) \land C = (\lnot A \lor B) \land C$

#### Step 2 - DNF Conversion

$$p_1 = A \land \lnot B$$

$$p_2 = (\lnot A \land C) \lor (B \land C)$$

#### Step 3 - Terms and Literals

For $p_1$:
- **Terms:** $\{A\lnot B\}$
- **Literals:** $A$, $\lnot B$

For $p_2$:
- **Terms:** $\{\lnot AC\}$, $\{BC\}$
- **Literals:** $\lnot A$, $C$, $B$

#### Step 4 - MUMCUT Analysis

##### For $p_1$: MUTP requirements

| Point | A | B | p1 |
|-------|---|---|----|
| MUTP-1 | T | F | T |

##### For $p_1$: CUTPNFP requirements

| Literal | Point | A | B | p1 |
|---------|-------|---|---|----|
| A | NFP-A | F | F | F |
| ¬B | NFP-B | T | T | F |

##### MNFP requirements

None for $p_1$.

#### Step 5 - Generated Test Requirements

For $p_1$ (sequence path):
1. MUTP-1: list value → sequence sub-validation
2. NFP-A: non-Sequence value → mapping path or no validation
3. NFP-B: string value → mapping path

For $p_2$ (mapping path):
1. Mapping value → mapping sub-validation

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 (p1) | `test_schema_sequence_value_valid` |
| NFP-B (p1) | `test_schema_mapping_value_valid` |
| p2 with error | `test_schema_mapping_value_invalid` |
| p1 with error | `test_schema_sequence_value_invalid` |

---

### 2.18 `_validate_contains`

**Function name:** `_validate_contains`

**Source predicate (line 1171):**
```python
if not isinstance(expected_values, Iterable) or isinstance(
    expected_values, _str_type
):
    expected_values = set((expected_values,))
else:
    expected_values = set(expected_values)
```

Let $A$ = `isinstance(expected_values, Iterable)`, $B$ = `isinstance(expected_values, _str_type)`.

#### Step 1 - Predicate Extraction

$$p = \lnot A \lor B$$

#### Step 2 - DNF Conversion

$$p = \lnot A \lor B$$

Two implicants: $\lnot A$ and $B$.

#### Step 3 - Terms and Literals

- **Terms:** $\{\lnot A\}$, $\{B\}$
- **Literals:** $\lnot A$, $B$
- **Major literals:** $\lnot A$ (unique to first), $B$ (unique to second)

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | Via | p |
|-------|---|---|-----|---|
| MUTP-¬A | F | F | ¬A | T |
| MUTP-B | T | T | B | T |

##### CUTPNFP requirements

| Implicant | Literal | NFP | A | B | p |
|-----------|---------|-----|---|---|---|
| ¬A | flip ¬A→A | NFP-¬A | T | F | F |
| B | flip B→¬B | NFP-B | T | F | F |

Both collapse to $(A=T, B=F)$: list expected values.

##### MNFP requirements

$(A=T, B=F)$: list used directly.

#### Step 5 - Generated Test Requirements

1. MUTP-¬A: scalar expected value → wrapped
2. MUTP-B: string expected value → treated as single value
3. NFP: list expected value → expanded as set

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-B | `test_contains_single_value_present` |
| NFP | `test_contains_list_expected_all_present` |

---

### 2.19 `_normalize_coerce`

**Function name:** `_normalize_coerce` (public normalizer)

**Source predicate (line 725):**
```python
if field in schema and 'coerce' in schema[field]:
    mapping[field] = self.__normalize_coerce(...)
```

Let $A$ = `field in schema`, $B$ = `'coerce' in schema[field]`.

#### Step 1 - Predicate Extraction

$$p = A \land B$$

#### Step 2 - DNF Conversion

$$p = A \land B$$

#### Step 3 - Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B | p |
|-------|---|---|---|
| MUTP-1 | T | T | T |

##### CUTPNFP requirements

| Literal | Point | A | B | p |
|---------|-------|---|---|---|
| A | NFP-A | F | T | F |
| B | NFP-B | T | F | F |

##### MNFP requirements

None.

#### Step 5 - Generated Test Requirements

1. MUTP-1: field in schema with coerce rule → coerce applied
2. NFP-A: field not in schema → skipped (elif branch checked)
3. NFP-B: field in schema, no coerce rule → not coerced

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_normalize_coerce_field_in_schema` |
| NFP-B | `test_normalize_coerce_no_coerce_rule` |

---

### 2.20 `_validate_items`

**Function name:** `_validate_items`

**Source predicate (line 1273):**
```python
if len(items) != len(values):
    self._error(field, errors.ITEMS_LENGTH, ...)
else:
    ...
    if not validator(...):
        self._error(field, errors.BAD_ITEMS, ...)
```

Let $A$ = `len(items) != len(values)`, $B_{pass}$ = child `validator()` returns True.

#### Step 1 - Predicate Extraction

$$p_1 = A \quad \text{(length mismatch error)}$$
$$p_2 = \lnot A \land \lnot B_{pass} \quad \text{(item validation error)}$$

#### Step 2 - DNF Conversion

$$p_1 = A$$
$$p_2 = \lnot A \land \lnot B_{pass}$$

#### Step 3 - Terms and Literals

For $p_1$: term $\{A\}$, literal $A$.
For $p_2$: term $\{\lnot A \lnot B_{pass}\}$, literals $\lnot A$, $\lnot B_{pass}$.

#### Step 4 - MUMCUT Analysis

##### MUTP requirements

| Point | A | B_pass | p1 | p2 |
|-------|---|--------|----|----|
| MUTP-p1 | T | — | T | — |
| MUTP-p2 | F | F | F | T |

##### CUTPNFP requirements

| Predicate | Literal | NFP | A | B_pass |
|-----------|---------|-----|---|--------|
| p1 | flip A→¬A | NFP-A | F | T | 
| p2 | flip ¬A→A | NFP-¬A | T | F |
| p2 | flip ¬B→B | NFP-¬B | F | T |

##### MNFP requirements

None beyond the CUTPNFPs.

#### Step 5 - Generated Test Requirements

1. MUTP-p1: mismatched lengths → ITEMS_LENGTH error
2. MUTP-p2: matched lengths, child fails → BAD_ITEMS error
3. NFP: matched lengths, child passes → no error

#### Step 6 - Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-p1 | `test_items_length_mismatch` |
| MUTP-p2 | `test_items_length_match_one_invalid` |
| NFP | `test_items_length_match_all_valid` |

---

## 3. DNF Fault Classes (Table 8.1) - Per-Member Analysis

Each member carries out one analysis per fault class as required.
Function references and tests are in `faults/mutations.md` and the corresponding test file.

### 3.1 Fault-class definitions

| Class | Description |
|-------|-------------|
| **LIF** | Literal Insertion Fault — a literal is replaced with `True` (clause short-circuited) |
| **LDF/LOF** | Literal Deletion/Omission Fault — a literal is removed from a term |
| **LRF** | Literal Replacement Fault — a literal's operator/constant is replaced with a related one |
| **LNF** | Literal Negation Fault — literal `c` replaced with `¬c` |
| **TOF** | Term Omission Fault — an entire implicant is removed from the DNF |
| **TNF** | Term Negation Fault — an implicant `t` is replaced with `¬t` |
| **TIF** | Term Insertion Fault — a spurious implicant is added to the DNF |
| **ORF+** | OR-to-AND Fault — a disjunction is replaced with a conjunction |
| **ORF\*** | AND-to-OR Fault — a conjunction is replaced with a disjunction |
| **ENF** | Expression Negation Fault — the entire predicate is negated |

### 3.2 Per-member fault-class coverage

| Fault Class | Member 1 function | Member 2 function | Member 3 function | Member 4 function |
|-------------|-------------------|-------------------|-------------------|-------------------|
| **LIF** | `_validate_type` (F1-1,F1-2) | `__normalize_coerce` (F2-2) | `_validate_empty` (F3-1) | `_normalize_coerce` (F4-4) |
| **LDF/LOF** | `_validate_minlength` (F1-6) | `_validate_maxlength` (F2-6) | `_validate_empty` (F3-6) | `_normalize_coerce` (F4-6) |
| **LRF** | `_validate_minlength` (F1-7) | `_validate_maxlength` (F2-5) | `_validate_empty` (F3-7) | `_validate_items` (F4-5) |
| **LNF** | `__validate_dependencies_mapping` (F1-5) | `__normalize_coerce` (F2-1) | `_validate_dependencies` (F3-2) | `_validate_schema` (F4-2) |
| **TOF** | `_validate_allowed` (F1-3) | `_validate_excludes` (F2-3) | `_validate_regex` (F3-4) | `_validate_forbidden` (F4-1) |
| **TNF** | `_validate_minlength` (F1-8) | `_validate_maxlength` (F2-7) | `_validate_empty` (F3-8) | `_normalize_coerce` (F4-7) |
| **TIF** | `_validate_allowed` (F1-9) | `_validate_maxlength` (F2-8) | `_validate_regex` (F3-9) | `_validate_forbidden` (F4-8) |
| **ORF+** | `__validate_dependencies_mapping` (F1-10) | `__normalize_coerce` (F2-9) | `_validate_dependencies` (F3-10) | `_validate_contains` (F4-9) |
| **ORF\*** | `_validate_minlength` (F1-11) | `_validate_excludes` (F2-10) | `_validate_regex` (F3-11) | `_validate_forbidden` (F4-10) |
| **ENF** | `_validate_allowed` (F1-12) | `_validate_maxlength` (F2-11) | `_validate_regex` (F3-5) | `_validate_forbidden` (F4-11) |

All 40 required analyses (4 members × 10 fault classes) are defined.
See `faults/mutations.md` for the exact original code, mutated code, rationale, and killing test for every entry.

---


## 4. Per-Member Fault-Class Coverage

The detailed MUMCUT derivations for the selected functions are already provided in Section 2.
The mapping between DNF fault classes and member responsibilities is provided in Section 3.2.

Detailed mutation definitions, fault-emulation rationale, and killing tests are documented in:
- faults/mutations.md
- tests/member1/
- tests/member2/
- tests/member3/
- tests/member4/

This section was intentionally condensed to avoid repeating the same six-step derivation pattern
for all 40 member × fault-class combinations.

---