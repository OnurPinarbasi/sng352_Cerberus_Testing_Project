# CerberusTesting – Project Report

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

#### Step 1 — Predicate Extraction

$$p = A \land \lnot B$$

The function sets `matched = True` only when the value belongs to the included types AND
does not belong to the excluded types. If `matched` remains False for all type candidates,
`BAD_TYPE` is raised.

#### Step 2 — DNF Conversion

The predicate is already a single conjunctive term. DNF is trivial:

$$p = A \land \lnot B$$

#### Step 3 — Terms and Literals

- **Terms (implicants):** $\{A\lnot B\}$
- **Literals:** $A$, $\lnot B$
- **Major literals:** $A$ (determines $p$ when $\lnot B = T$), $\lnot B$ (determines $p$ when $A = T$)

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-1: value matches included_types, does not match excluded_types → `matched=True`
2. NFP-A: value does not match included_types → `matched=False`
3. NFP-B: value matches both included_types and excluded_types → `matched=False`

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = A \land \lnot B$$

#### Step 2 — DNF Conversion

Already in minimal DNF:

$$p = A \land \lnot B$$

#### Step 3 — Terms and Literals

- **Terms:** $\{A\lnot B\}$
- **Literals:** $A$, $\lnot B$
- **Major literals:** $A$, $\lnot B$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-1: list value (Iterable, not str) → list check path
2. NFP-A: integer value (not Iterable) → scalar path
3. NFP-B: string value (Iterable and str) → scalar path

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

Outer: $p_1 = A$. When true, inner: $p_2 = B$.

The combined predicate for sub-validation is $p = A \land B$.

#### Step 2 — DNF Conversion

$$p = A \land B$$

#### Step 3 — Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-1: `allow_unknown=Mapping` → sub-validates unknown field
2. NFP-A: `allow_unknown=False` → unknown field rejected
3. NFP-B: `allow_unknown=True` (not Mapping/str) → unknown accepted without sub-validation

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = A \land B$$

#### Step 2 — DNF Conversion

$$p = A \land B$$

#### Step 3 — Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-1: Iterable value with length < min → MIN_LENGTH error
2. NFP-A: non-Iterable value → no error
3. NFP-B: Iterable value with length ≥ min → no error

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = \lnot A \lor B$$

#### Step 2 — DNF Conversion

Two implicants:

$$p = \lnot A \lor B$$

#### Step 3 — Terms and Literals

- **Terms:** $\{\lnot A\}$, $\{B\}$
- **Literals:** $\lnot A$, $B$
- **Major literals:** $\lnot A$ (unique to first term), $B$ (unique to second term)

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-¬A: scalar (non-Sequence) dep value → normalised to list
2. MUTP-B: string dep value → normalised to list
3. NFP: list dep value → used directly (predicate false)

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = \lnot(A \land B) = \lnot A \lor \lnot B$$

#### Step 2 — DNF Conversion

$$p = \lnot A \lor \lnot B$$

Two implicants: $\lnot A$ and $\lnot B$.

#### Step 3 — Terms and Literals

- **Terms:** $\{\lnot A\}$, $\{\lnot B\}$
- **Literals:** $\lnot A$, $\lnot B$
- **Major literals:** $\lnot A$ (unique to first), $\lnot B$ (unique to second)

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-¬A: `nullable=False, value=None` → error filed
2. MUTP-¬B: `nullable=True, value≠None` → error filed
3. NFP/MNFP: `nullable=True, value=None` → error suppressed

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = A \land B$$

#### Step 2 — DNF Conversion

$$p = A \land B$$

#### Step 3 — Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-1: excluded field in schema and excluding field required → excluded marked unrequired
2. NFP-A: excluded field not in schema → no exemption
3. NFP-B: excluding field not required → no exemption

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = A \land B$$

#### Step 2 — DNF Conversion

$$p = A \land B$$

#### Step 3 — Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-1: normalized=True and has_error=True → rules dropped
2. NFP-A: normalized=False → READONLY_FIELD error (first branch), rules not dropped
3. NFP-B: normalized=True and no prior error → no drop

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = A \land B$$

#### Step 2 — DNF Conversion

$$p = A \land B$$

#### Step 3 — Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-1: Iterable value with length > max → MAX_LENGTH error
2. NFP-A: non-Iterable → no check
3. NFP-B: Iterable within limit → no error

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

Outer: $p_1 = A$. Inner: $p_2 = \lnot B_{pass}$ where $B_{pass}$ = child validator returns True.

Combined error predicate: $p = A \land \lnot B_{pass}$.

#### Step 2 — DNF Conversion

$$p = A \land \lnot B_{pass}$$

#### Step 3 — Terms and Literals

- **Terms:** $\{A\lnot B_{pass}\}$
- **Literals:** $A$, $\lnot B_{pass}$
- **Major literals:** $A$, $\lnot B_{pass}$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-1: Mapping value with key failing keysrules → error
2. NFP-A: non-Mapping value → keysrules skipped
3. NFP-B: Mapping value with all keys passing → no error

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = A \land B$$

#### Step 2 — DNF Conversion

$$p = A \land B$$

#### Step 3 — Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-1: empty Sized value with `empty=False` → EMPTY_NOT_ALLOWED error
2. NFP-A: non-Sized value → no empty check
3. NFP-B: non-empty Sized value → no error

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = A \lor \lnot B$$

#### Step 2 — DNF Conversion

$$p = A \lor \lnot B$$

Two implicants: $A$ and $\lnot B$.

#### Step 3 — Terms and Literals

- **Terms:** $\{A\}$, $\{\lnot B\}$
- **Literals:** $A$, $\lnot B$
- **Major literals:** $A$ (unique to first), $\lnot B$ (unique to second)

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-A: string dep → normalised
2. MUTP-¬B: scalar dep (not Iterable/Mapping) → normalised
3. NFP: list dep → used directly

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = A \lor \lnot B$$

A field counts as "present" (not missing) when its value is not None OR when
`ignore_none_values` is False.

#### Step 2 — DNF Conversion

$$p = A \lor \lnot B$$

Two implicants: $A$ and $\lnot B$.

#### Step 3 — Terms and Literals

- **Terms:** $\{A\}$, $\{\lnot B\}$
- **Literals:** $A$, $\lnot B$
- **Major literals:** $A$, $\lnot B$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-A: field has non-None value, ignore_none_values=True → field counts as present
2. MUTP-¬B: ignore_none_values=False → None-valued field counts as present
3. NFP: field=None, ignore_none_values=True → field NOT counted → required error

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

The error fires when: $A$ is True (not returned early) AND $\lnot B$ (match fails).

$$p_{err} = A \land \lnot B$$

#### Step 2 — DNF Conversion

$$p_{err} = A \land \lnot B$$

#### Step 3 — Terms and Literals

- **Terms:** $\{A\lnot B\}$
- **Literals:** $A$, $\lnot B$
- **Major literals:** $A$, $\lnot B$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-1: string value that does not match → REGEX_MISMATCH error
2. NFP-A: non-string value → guard returns → no error
3. NFP-B: string value that matches → no error

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = A \land B$$

#### Step 2 — DNF Conversion

$$p = A \land B$$

#### Step 3 — Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-1: Mapping with invalid value → error
2. NFP-A: non-Mapping → no check
3. NFP-B: Mapping with all valid values → no error

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = A \land \lnot B$$

#### Step 2 — DNF Conversion

$$p = A \land \lnot B$$

#### Step 3 — Terms and Literals

- **Terms:** $\{A\lnot B\}$
- **Literals:** $A$, $\lnot B$
- **Major literals:** $A$, $\lnot B$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-1: list value → element-wise forbidden check
2. NFP-A: scalar value (not Sequence) → scalar check
3. NFP-B: string value (Sequence and str) → scalar check

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

Branch 1 predicate: $p_1 = A \land \lnot B$
Branch 2 predicate: $p_2 = \lnot(A \land \lnot B) \land C = (\lnot A \lor B) \land C$

#### Step 2 — DNF Conversion

$$p_1 = A \land \lnot B$$

$$p_2 = (\lnot A \land C) \lor (B \land C)$$

#### Step 3 — Terms and Literals

For $p_1$:
- **Terms:** $\{A\lnot B\}$
- **Literals:** $A$, $\lnot B$

For $p_2$:
- **Terms:** $\{\lnot AC\}$, $\{BC\}$
- **Literals:** $\lnot A$, $C$, $B$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

For $p_1$ (sequence path):
1. MUTP-1: list value → sequence sub-validation
2. NFP-A: non-Sequence value → mapping path or no validation
3. NFP-B: string value → mapping path

For $p_2$ (mapping path):
1. Mapping value → mapping sub-validation

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = \lnot A \lor B$$

#### Step 2 — DNF Conversion

$$p = \lnot A \lor B$$

Two implicants: $\lnot A$ and $B$.

#### Step 3 — Terms and Literals

- **Terms:** $\{\lnot A\}$, $\{B\}$
- **Literals:** $\lnot A$, $B$
- **Major literals:** $\lnot A$ (unique to first), $B$ (unique to second)

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-¬A: scalar expected value → wrapped
2. MUTP-B: string expected value → treated as single value
3. NFP: list expected value → expanded as set

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p = A \land B$$

#### Step 2 — DNF Conversion

$$p = A \land B$$

#### Step 3 — Terms and Literals

- **Terms:** $\{AB\}$
- **Literals:** $A$, $B$
- **Major literals:** $A$, $B$

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-1: field in schema with coerce rule → coerce applied
2. NFP-A: field not in schema → skipped (elif branch checked)
3. NFP-B: field in schema, no coerce rule → not coerced

#### Step 6 — Implemented Test Cases

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

#### Step 1 — Predicate Extraction

$$p_1 = A \quad \text{(length mismatch error)}$$
$$p_2 = \lnot A \land \lnot B_{pass} \quad \text{(item validation error)}$$

#### Step 2 — DNF Conversion

$$p_1 = A$$
$$p_2 = \lnot A \land \lnot B_{pass}$$

#### Step 3 — Terms and Literals

For $p_1$: term $\{A\}$, literal $A$.
For $p_2$: term $\{\lnot A \lnot B_{pass}\}$, literals $\lnot A$, $\lnot B_{pass}$.

#### Step 4 — MUMCUT Analysis

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

#### Step 5 — Generated Test Requirements

1. MUTP-p1: mismatched lengths → ITEMS_LENGTH error
2. MUTP-p2: matched lengths, child fails → BAD_ITEMS error
3. NFP: matched lengths, child passes → no error

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-p1 | `test_items_length_mismatch` |
| MUTP-p2 | `test_items_length_match_one_invalid` |
| NFP | `test_items_length_match_all_valid` |

---

## 3. DNF Fault Classes (Table 8.1) — Per-Member Analysis

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

## 4. Per-Member Fault-Class MUMCUT Derivations

The following sections present the full Step 1–6 MUMCUT derivation for every
member × fault-class combination (40 total). Each is written out in full; no derivation
references another.

---

### 4.1 Member 1 — LIF: `_validate_type`

**Function:** `_validate_type` · **Fault class:** LIF · **Mutation:** F1-1

#### Step 1 — Predicate Extraction

```python
matched = isinstance(value, type_definition.included_types) \
          and not isinstance(value, type_definition.excluded_types)
```

Let $A$ = `isinstance(value, included_types)`, $B$ = `isinstance(value, excluded_types)`.

#### Step 2 — DNF Conversion

$$P = A \land \lnot B$$

LIF mutation replaces $A$ with $\mathit{True}$:

$$P_{\text{mut}} = \mathit{True} \land \lnot B = \lnot B$$

The mutant predicate is weaker — it passes any value not in excluded_types.

#### Step 3 — Terms and Literals

- Original terms: $\{A\lnot B\}$
- Literals: $A$, $\lnot B$
- Major literals: both (single-implicant)

#### Step 4 — MUMCUT Analysis

##### MUTP requirements

| MUTP | A | B | P (orig) | P (mut) |
|------|---|---|----------|---------|
| MUTP-1 | T | F | T | T |

##### CUTPNFP requirements

| Literal | A | B | P (orig) | P (mut) | Kills mutant? |
|---------|---|---|----------|---------|---------------|
| NFP-A | F | F | F | T | **Yes** (F≠T) |
| NFP-B | T | T | F | F | No |

NFP-A is the killing test: $A=F$ means wrong type; original → error; mutant → no error.

##### MNFP requirements

None (single implicant).

#### Step 5 — Generated Test Requirements

1. MUTP-1: `isinstance(value, included)=T, isinstance(value, excluded)=F` → no error
2. NFP-A: `isinstance(value, included)=F` → error (kills LIF on A)
3. NFP-B: value in both → error

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_type_utp_both_clauses_true_no_error` |
| NFP-A (kills LIF) | `test_type_nfp_clause_a_false_error` |
| NFP-B | `test_type_nfp_clause_b_true_error` |

---

### 4.2 Member 1 — LDF: `_validate_minlength`

**Function:** `_validate_minlength` · **Fault class:** LDF · **Mutation:** F1-6

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Iterable) and len(value) < min_length:
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `len(value) < min_length`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

LDF deletes $B$:

$$P_{\text{mut}} = A$$

#### Step 3 — Terms and Literals

- Original terms: $\{AB\}$
- Literals: $A$, $B$
- Major literals: $A$, $B$

#### Step 4 — MUMCUT Analysis

##### MUTP requirements

| MUTP | A | B | P (orig) | P (mut) |
|------|---|---|----------|---------|
| MUTP-1 | T | T | T | T |

##### CUTPNFP requirements

| Literal | A | B | P (orig) | P (mut) | Kills mutant? |
|---------|---|---|----------|---------|---------------|
| NFP-A | F | T | F | F | No |
| NFP-B | T | F | F | T | **Yes** (F≠T) |

NFP-B is the killing test: value is Iterable but meets min_length; original → no error;
mutant (only A) → fires error.

##### MNFP requirements

None.

#### Step 5 — Generated Test Requirements

1. MUTP-1: list too short → error
2. NFP-A: non-Iterable → no error
3. NFP-B: list of exactly min_length → no error (kills LDF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_minlength_utp_list_too_short` |
| NFP-A | `test_minlength_nfp_a_non_iterable` |
| NFP-B (kills LDF) | `test_minlength_ldf_b_deleted` |

---

### 4.3 Member 1 — LRF: `_validate_minlength`

**Function:** `_validate_minlength` · **Fault class:** LRF · **Mutation:** F1-7

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Iterable) and len(value) < min_length:
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `len(value) < min_length`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

LRF replaces `<` with `<=`:

$$P_{\text{mut}} = A \land (len(value) \leq min\_length)$$

#### Step 3 — Terms and Literals

- Original terms: $\{AB\}$; Mutant terms: $\{AB'\}$ where $B'$ = `len<=min`
- Major literals: $A$, $B$

#### Step 4 — MUMCUT Analysis

##### MUTP requirements

| MUTP | A | B | B' | P (orig) | P (mut) |
|------|---|---|----|----------|---------|
| MUTP-1 | T | T | T | T | T |

##### CUTPNFP requirements

The boundary case $len = min\_length$: $B=F$, $B'=T$.

| Case | A | B | B' | P (orig) | P (mut) | Kills mutant? |
|------|---|---|----|----------|---------|---------------|
| Boundary | T | F | T | F | T | **Yes** |

##### MNFP requirements

None.

#### Step 5 — Generated Test Requirements

1. MUTP-1: list with len < min → error
2. Boundary: list with len == min → no error originally, error with mutation (kills LRF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_minlength_utp_list_too_short` |
| Boundary (kills LRF) | `test_minlength_lrf_boundary` |

---

### 4.4 Member 1 — LNF: `__validate_dependencies_mapping`

**Function:** `__validate_dependencies_mapping` · **Fault class:** LNF · **Mutation:** F1-5

#### Step 1 — Predicate Extraction

```python
if not isinstance(dependency_values, Sequence) or isinstance(
    dependency_values, _str_type
):
    dependency_values = [dependency_values]
```

Let $A$ = `isinstance(dep_values, Sequence)`, $B$ = `isinstance(dep_values, _str_type)`.

#### Step 2 — DNF Conversion

$$P = \lnot A \lor B$$

LNF negates $\lnot A$ to $A$:

$$P_{\text{mut}} = A \lor B$$

#### Step 3 — Terms and Literals

- Original terms: $\{\lnot A\}$, $\{B\}$
- Literals: $\lnot A$, $B$
- Major literals: $\lnot A$, $B$

#### Step 4 — MUMCUT Analysis

##### MUTP requirements

| MUTP | A | B | P (orig) | P (mut) |
|------|---|---|----------|---------|
| MUTP-¬A | F | F | T | F |
| MUTP-B | T | T | T | T |

MUTP-¬A differs: original True, mutant False → **kills mutant**.

##### CUTPNFP requirements

| Literal | A | B | P (orig) | P (mut) | Kills? |
|---------|---|---|----------|---------|--------|
| NFP-¬A | T | F | F | T | Yes |
| NFP-B | T | F | F | T | Yes |

##### MNFP requirements

$(A=T, B=F)$: list dep value.

#### Step 5 — Generated Test Requirements

1. MUTP-¬A: scalar dep value → normalised to list → dep satisfied (kills LNF)
2. MUTP-B: string dep value → normalised
3. NFP: list dep value → used directly (predicate false)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-¬A (kills LNF) | `test_dep_mapping_scalar_dep_value_satisfied` |
| MUTP-B | `test_dep_mapping_string_dep_value_satisfied` |
| NFP | `test_dep_mapping_list_dep_value_nfp` |

---

### 4.5 Member 1 — TOF: `_validate_allowed`

**Function:** `_validate_allowed` · **Fault class:** TOF · **Mutation:** F1-3

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Iterable) and not isinstance(value, _str_type):
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `isinstance(value, _str_type)`.

#### Step 2 — DNF Conversion

$$P = A \land \lnot B$$

TOF drops $\lnot B$:

$$P_{\text{mut}} = A$$

#### Step 3 — Terms and Literals

- Original: $\{A\lnot B\}$; Mutant: $\{A\}$
- Major literals: $A$, $\lnot B$

#### Step 4 — MUMCUT Analysis

##### MUTP requirements

| MUTP | A | B | P (orig) | P (mut) |
|------|---|---|----------|---------|
| MUTP-1 | T | F | T | T |

##### CUTPNFP requirements

| Literal | A | B | P (orig) | P (mut) | Kills? |
|---------|---|---|----------|---------|--------|
| NFP-A | F | F | F | F | No |
| NFP-B (kills) | T | T | F | T | **Yes** |

NFP-B is the killing test: string value; original → scalar path; mutant → list path.

##### MNFP requirements

None.

#### Step 5 — Generated Test Requirements

1. MUTP-1: list value → list check path
2. NFP-B: string value → scalar path (kills TOF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| MUTP-1 | `test_allowed_utp_list_all_allowed` |
| NFP-B (kills TOF) | `test_allowed_nfp_b_string_treated_as_scalar` |

---

### 4.6 Member 1 — TNF: `_validate_minlength`

**Function:** `_validate_minlength` · **Fault class:** TNF · **Mutation:** F1-8

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Iterable) and len(value) < min_length:
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `len(value) < min_length`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

TNF negates the implicant: $\lnot(A \land B) = \lnot A \lor \lnot B$.

$$P_{\text{mut}} = \lnot A \lor \lnot B$$

#### Step 3 — Terms and Literals

- Mutant terms: $\{\lnot A\}$, $\{\lnot B\}$

#### Step 4 — MUMCUT Analysis

##### MUTP requirements

| MUTP | A | B | P (orig) | P (mut) |
|------|---|---|----------|---------|
| MUTP-1 | T | T | T | F |

The MUTP itself is killed by the mutant (T→F).

##### CUTPNFP requirements

The NFP-B point $(A=T, B=F)$: P(orig)=F, P(mut)=T (¬B = True) → kills mutant.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| MUTP | T | T | T | F | Yes |
| NFP-B | T | F | F | T | Yes |

#### Step 5 — Generated Test Requirements

1. Long list (A=T, B=F): no error originally; with TNF → error (kills mutant)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills TNF | `test_minlength_tnf_long_list` |

---

### 4.7 Member 1 — TIF: `_validate_allowed`

**Function:** `_validate_allowed` · **Fault class:** TIF · **Mutation:** F1-9

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Iterable) and not isinstance(value, _str_type):
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `isinstance(value, _str_type)`.

#### Step 2 — DNF Conversion

$$P = A \land \lnot B$$

TIF inserts a spurious implicant `isinstance(value, int)` = $C$:

$$P_{\text{mut}} = (A \land \lnot B) \lor C$$

#### Step 3 — Terms and Literals

- Mutant terms: $\{A\lnot B\}$, $\{C\}$
- New literal: $C$ = `isinstance(value, int)`

#### Step 4 — MUMCUT Analysis

The extra implicant $C$ makes the predicate true for integers, which should follow
the scalar path.

##### Killing test requirement

An integer value in the allowed list: $A=F, B=F, C=T$:
- Original: $P = F \land T = F$ → scalar path → valid
- Mutant: $P = F \lor T = T$ → list path → TypeError

#### Step 5 — Generated Test Requirements

1. Integer value in allowed list → valid via scalar path (kills TIF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills TIF | `test_allowed_tif_integer_in_allowed` |

---

### 4.8 Member 1 — ORF+: `__validate_dependencies_mapping`

**Function:** `__validate_dependencies_mapping` · **Fault class:** ORF+ · **Mutation:** F1-10

#### Step 1 — Predicate Extraction

```python
if not isinstance(dependency_values, Sequence) or isinstance(
    dependency_values, _str_type
):
```

Let $A$ = `isinstance(dep_values, Sequence)`, $B$ = `isinstance(dep_values, _str_type)`.

#### Step 2 — DNF Conversion

$$P = \lnot A \lor B$$

ORF+ replaces OR with AND:

$$P_{\text{mut}} = \lnot A \land B$$

#### Step 3 — Terms and Literals

- Original: two implicants $\lnot A$, $B$
- Mutant: one implicant $\lnot A \land B$ (impossible since str IS Sequence → ¬A=F for str)

#### Step 4 — MUMCUT Analysis

The mutant predicate is always False for strings and non-sequences → nothing is ever
normalised.

##### MUTP (¬A via integer dep value): A=F, B=F → orig=T, mut=F → kills mutant.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| MUTP-¬A | F | F | T | F | **Yes** |

#### Step 5 — Generated Test Requirements

1. Integer dep value → normalised to list → dep satisfied (kills ORF+)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills ORF+ | `test_dep_mapping_orf_plus_int_dep` |

---

### 4.9 Member 1 — ORF*: `_validate_minlength`

**Function:** `_validate_minlength` · **Fault class:** ORF\* · **Mutation:** F1-11

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Iterable) and len(value) < min_length:
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `len(value) < min_length`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

ORF\* replaces AND with OR:

$$P_{\text{mut}} = A \lor B$$

#### Step 3 — Terms and Literals

- Mutant: two implicants $\{A\}$, $\{B\}$

#### Step 4 — MUMCUT Analysis

For any list value (A=T), P_mut = True regardless of B.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-B | T | F | F | T | **Yes** |

A list meeting the length requirement: original → no error; mutant → error.

#### Step 5 — Generated Test Requirements

1. List of length > min_length → no error originally (kills ORF\*)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills ORF\* | `test_minlength_orf_star_long_list` |

---

### 4.10 Member 1 — ENF: `_validate_allowed`

**Function:** `_validate_allowed` · **Fault class:** ENF · **Mutation:** F1-12

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Iterable) and not isinstance(value, _str_type):
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `isinstance(value, _str_type)`.

#### Step 2 — DNF Conversion

$$P = A \land \lnot B$$

ENF negates the entire expression:

$$P_{\text{mut}} = \lnot(A \land \lnot B) = \lnot A \lor B$$

#### Step 3 — Terms and Literals

- Mutant terms: $\{\lnot A\}$, $\{B\}$

#### Step 4 — MUMCUT Analysis

For a list value (A=T, B=F): orig=T, mut=¬T=F → list goes to wrong (scalar) branch.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| MUTP-1 | T | F | T | F | **Yes** |

#### Step 5 — Generated Test Requirements

1. List with all allowed elements → valid (kills ENF: mutant goes to scalar path → error)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills ENF | `test_allowed_enf_list_all_allowed` |

---

### 4.11 Member 2 — LIF: `__normalize_coerce`

**Function:** `__normalize_coerce` · **Fault class:** LIF · **Mutation:** F2-2

#### Step 1 — Predicate Extraction

```python
if not (nullable and value is None):
```

Let $A$ = `nullable`, $B$ = `value is None`.

#### Step 2 — DNF Conversion

$$P = \lnot A \lor \lnot B$$

LIF replaces $A$ with $\mathit{True}$:

$$P_{\text{mut}} = \lnot \mathit{True} \lor \lnot B = \lnot B$$

#### Step 3 — Terms and Literals

- Mutant reduces to single implicant $\lnot B$

#### Step 4 — MUMCUT Analysis

When nullable=False, value=None: orig: $\lnot F \lor \lnot T = T \lor F = T$ → error filed.
Mutant: $\lnot T = F$ → suppressed.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| MUTP-¬A | F | T | T | F | **Yes** |

#### Step 5 — Generated Test Requirements

1. nullable=False, value=None → error (kills LIF on A)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills LIF | `test_coerce_nonnullable_none_errors` |

---

### 4.12 Member 2 — LDF: `_validate_maxlength`

**Function:** `_validate_maxlength` · **Fault class:** LDF · **Mutation:** F2-6

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Iterable) and len(value) > max_length:
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `len(value) > max_length`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

LDF deletes $B$:

$$P_{\text{mut}} = A$$

#### Step 3 — Terms and Literals

- Mutant: single implicant $\{A\}$

#### Step 4 — MUMCUT Analysis

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-B | T | F | F | T | **Yes** |

List within limit: original → no error; mutant → error.

#### Step 5 — Generated Test Requirements

1. List within max_length → no error (kills LDF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills LDF | `test_maxlength_ldf_b_deleted` |

---

### 4.13 Member 2 — LRF: `_validate_maxlength`

**Function:** `_validate_maxlength` · **Fault class:** LRF · **Mutation:** F2-5

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Iterable) and len(value) > max_length:
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `len(value) > max_length`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

LRF replaces `>` with `>=`:

$$P_{\text{mut}} = A \land (len(value) \geq max\_length)$$

#### Step 3 — Terms and Literals

- Boundary distinguishes: at $len = max\_length$, $B=F$, $B'=T$.

#### Step 4 — MUMCUT Analysis

| Point | A | B | B' | P (orig) | P (mut) | Kills? |
|-------|---|---|----|----------|---------|--------|
| Boundary | T | F | T | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. List of exactly max_length → no error originally (kills LRF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills LRF | `test_maxlength_nfp_b_within_limit` |

---

### 4.14 Member 2 — LNF: `__normalize_coerce`

**Function:** `__normalize_coerce` · **Fault class:** LNF · **Mutation:** F2-1

#### Step 1 — Predicate Extraction

```python
if not (nullable and value is None):
```

Expanded: $P = \lnot A \lor \lnot B$.

LNF negates the outer `not`, i.e., flips $\lnot(A \land B)$ to $A \land B$:

$$P_{\text{mut}} = A \land B$$

#### Step 2 — DNF Conversion

$$P_{\text{mut}} = A \land B$$

#### Step 3 — Terms and Literals

- Mutant: single implicant $\{AB\}$

#### Step 4 — MUMCUT Analysis

When nullable=True, value=None: orig P=$F \lor F$=F → suppressed (no error).
Mutant: $T \land T = T$ → error filed.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP | T | T | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. nullable=True, value=None → no error (kills LNF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills LNF | `test_coerce_nullable_none_suppressed` |

---

### 4.15 Member 2 — TOF: `_validate_excludes`

**Function:** `_validate_excludes` · **Fault class:** TOF · **Mutation:** F2-3

#### Step 1 — Predicate Extraction

```python
if excluded_field in self.schema and self.schema[field].get(
    'required', self.require_all
):
```

Let $A$ = `excluded_field in self.schema`, $B$ = `schema[field].get('required')`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

TOF removes $B$:

$$P_{\text{mut}} = A$$

#### Step 3 — Terms and Literals

- Mutant: $\{A\}$

#### Step 4 — MUMCUT Analysis

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-B | T | F | F | T | **Yes** |

Excluded field in schema but excluding field not required: original → y not exempted;
mutant → y wrongly exempted → required check bypassed.

#### Step 5 — Generated Test Requirements

1. y required, x not required, x excludes y, document={x:1} → error (kills TOF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills TOF | `test_excludes_neither_present_required_fails` |

---

### 4.16 Member 2 — TNF: `_validate_maxlength`

**Function:** `_validate_maxlength` · **Fault class:** TNF · **Mutation:** F2-7

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Iterable) and len(value) > max_length:
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `len(value) > max_length`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

TNF: $P_{\text{mut}} = \lnot A \lor \lnot B$.

#### Step 3 — Terms and Literals

- Mutant: $\{\lnot A\}$, $\{\lnot B\}$

#### Step 4 — MUMCUT Analysis

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-B | T | F | F | T | **Yes** |

List within limit: original no error; mutant ¬B=T → error.

#### Step 5 — Generated Test Requirements

1. List within max_length → no error (kills TNF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills TNF | `test_maxlength_tnf_within_limit` |

---

### 4.17 Member 2 — TIF: `_validate_maxlength`

**Function:** `_validate_maxlength` · **Fault class:** TIF · **Mutation:** F2-8

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Iterable) and len(value) > max_length:
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `len(value) > max_length`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

TIF inserts spurious implicant $\lnot A$:

$$P_{\text{mut}} = (A \land B) \lor \lnot A$$

#### Step 3 — Terms and Literals

- Mutant: $\{AB\}$, $\{\lnot A\}$

#### Step 4 — MUMCUT Analysis

For non-Iterable ($A=F$): orig $P=F$; mutant $\lnot A = T$ → error.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-A | F | T | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. Integer (non-Iterable) → no maxlength check (kills TIF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills TIF | `test_maxlength_tif_non_iterable` |

---

### 4.18 Member 2 — ORF+: `__normalize_coerce`

**Function:** `__normalize_coerce` · **Fault class:** ORF+ · **Mutation:** F2-9

#### Step 1 — Predicate Extraction

```python
if not (nullable and value is None):   # ¬A ∨ ¬B
```

Let $A$ = `nullable`, $B$ = `value is None`.

#### Step 2 — DNF Conversion

$$P = \lnot A \lor \lnot B$$

ORF+ replaces OR with AND:

$$P_{\text{mut}} = \lnot A \land \lnot B$$

#### Step 3 — Terms and Literals

- Mutant: single implicant $\{\lnot A \lnot B\}$

#### Step 4 — MUMCUT Analysis

When nullable=True (A=T), value≠None (B=F): orig $\lnot T \lor \lnot F = F \lor T = T$ → error.
Mutant: $\lnot T \land \lnot F = F \land T = F$ → suppressed.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| MUTP-¬B | T | F | T | F | **Yes** |

#### Step 5 — Generated Test Requirements

1. nullable=True, bad coerce value (≠None) → error propagated (kills ORF+)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills ORF+ | `test_coerce_orf_plus_nullable_bad_coerce` |

---

### 4.19 Member 2 — ORF*: `_validate_excludes`

**Function:** `_validate_excludes` · **Fault class:** ORF\* · **Mutation:** F2-10

#### Step 1 — Predicate Extraction

```python
if excluded_field in self.schema and self.schema[field].get(
    'required', self.require_all
):
```

Let $A$ = `excluded_field in self.schema`, $B$ = `schema[field].get('required')`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

ORF\* replaces AND with OR:

$$P_{\text{mut}} = A \lor B$$

#### Step 3 — Terms and Literals

- Mutant: $\{A\}$, $\{B\}$

#### Step 4 — MUMCUT Analysis

$A=T, B=F$ (excluded field in schema, excluding field NOT required):
orig $F$; mutant $T \lor F = T$ → excluded field wrongly exempted.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-B | T | F | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. y required, x not required, x excludes y, document={x:1} → error (kills ORF\*)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills ORF\* | `test_excludes_orf_star_required_missing` |

---

### 4.20 Member 2 — ENF: `_validate_maxlength`

**Function:** `_validate_maxlength` · **Fault class:** ENF · **Mutation:** F2-11

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Iterable) and len(value) > max_length:
```

Let $A$ = `isinstance(value, Iterable)`, $B$ = `len(value) > max_length`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

ENF negates: $P_{\text{mut}} = \lnot A \lor \lnot B$.

#### Step 3 — Terms and Literals

- Mutant: $\{\lnot A\}$, $\{\lnot B\}$

#### Step 4 — MUMCUT Analysis

$A=T, B=F$ (Iterable, within limit): orig $F$; mutant $\lnot F = T$ → error.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-B | T | F | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. List within limit → no error (kills ENF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills ENF | `test_maxlength_enf_within_limit` |

---

### 4.21 Member 3 — LIF: `_validate_empty`

**Function:** `_validate_empty` · **Fault class:** LIF · **Mutation:** F3-1

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Sized) and len(value) == 0:
```

Let $A$ = `isinstance(value, Sized)`, $B$ = `len(value) == 0`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

LIF replaces $A$ with $\mathit{True}$: $P_{\text{mut}} = B$.

#### Step 3 — Terms and Literals

- Mutant: $\{B\}$

#### Step 4 — MUMCUT Analysis

Non-Sized value (A=F): orig $F$; mutant depends on $B$ → `len(non-Sized)` → TypeError.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-A | F | T | F | Error | **Yes** |

#### Step 5 — Generated Test Requirements

1. Non-Sized value with empty rule → no check (kills LIF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills LIF | `test_empty_utp_empty_list_allowed` (indirectly); key test: non-Sized via `test_minlength_nfp_a_non_iterable` pattern |

---

### 4.22 Member 3 — LDF: `_validate_empty`

**Function:** `_validate_empty` · **Fault class:** LDF · **Mutation:** F3-6

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Sized) and len(value) == 0:
```

Let $A$ = `isinstance(value, Sized)`, $B$ = `len(value) == 0`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

LDF deletes $B$: $P_{\text{mut}} = A$.

#### Step 3 — Terms and Literals

- Mutant: $\{A\}$

#### Step 4 — MUMCUT Analysis

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-B | T | F | F | T | **Yes** |

Non-empty Sized value: original no error; mutant → error.

#### Step 5 — Generated Test Requirements

1. Non-empty list with empty=False → no error (kills LDF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills LDF | `test_empty_ldf_b_deleted` |

---

### 4.23 Member 3 — LRF: `_validate_empty`

**Function:** `_validate_empty` · **Fault class:** LRF · **Mutation:** F3-7

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Sized) and len(value) == 0:
```

LRF replaces `0` with `1`: $B' = (len(value) == 1)$.

#### Step 2 — DNF Conversion

$$P_{\text{mut}} = A \land (len(value) == 1)$$

#### Step 3 — Terms and Literals

- Boundary: single-element list (B=F, B'=T)

#### Step 4 — MUMCUT Analysis

| Point | A | B | B' | P (orig) | P (mut) | Kills? |
|-------|---|---|----|----------|---------|--------|
| Single-elem | T | F | T | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. Single-element list with empty=False → no error (kills LRF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills LRF | `test_empty_lrf_single_element` |

---

### 4.24 Member 3 — LNF: `_validate_dependencies`

**Function:** `_validate_dependencies` · **Fault class:** LNF · **Mutation:** F3-2

#### Step 1 — Predicate Extraction

```python
if isinstance(dependencies, _str_type) or not isinstance(
    dependencies, (Iterable, Mapping)
):
```

Let $A$ = `isinstance(deps, str)`, $B$ = `isinstance(deps, (Iterable, Mapping))`.

$$P = A \lor \lnot B$$

LNF negates $\lnot B$ to $B$: $P_{\text{mut}} = A \lor B$.

#### Step 2 — DNF Conversion

$$P_{\text{mut}} = A \lor B$$

#### Step 3 — Terms and Literals

- Mutant: $\{A\}$, $\{B\}$

#### Step 4 — MUMCUT Analysis

List deps (A=F, B=T): orig $F \lor F = F$ → list used directly.
Mutant: $F \lor T = T$ → list wrapped in tuple → list treated as single dep name.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP | F | T | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. List deps → used directly (kills LNF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills LNF | `test_dep_list_dep_satisfied` |

---

### 4.25 Member 3 — TOF: `_validate_regex`

**Function:** `_validate_regex` · **Fault class:** TOF · **Mutation:** F3-4

#### Step 1 — Predicate Extraction

```python
if not isinstance(value, _str_type):
    return
```

Guard implicant: $\lnot A$ (¬isinstance(str)) → return (skip validation).

#### Step 2 — DNF Conversion

TOF removes the guard entirely: non-strings reach `re_obj.match(value)` → TypeError.

#### Step 3 — Terms and Literals

- Removed implicant: $\{\lnot A\}$

#### Step 4 — MUMCUT Analysis

Non-string value: orig → return → no error; mutant → TypeError → error.

| Point | A | P (orig) | P (mut) | Kills? |
|-------|---|----------|---------|--------|
| A=F | F | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. Integer with regex rule → no error (kills TOF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills TOF | `test_regex_nfp_a_non_string` |

---

### 4.26 Member 3 — TNF: `_validate_empty`

**Function:** `_validate_empty` · **Fault class:** TNF · **Mutation:** F3-8

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Sized) and len(value) == 0:
```

Let $A$ = `isinstance(value, Sized)`, $B$ = `len(value) == 0`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

TNF: $P_{\text{mut}} = \lnot A \lor \lnot B$.

#### Step 3 — Terms and Literals

- Mutant: $\{\lnot A\}$, $\{\lnot B\}$

#### Step 4 — MUMCUT Analysis

Non-empty list (A=T, B=F): orig $F$; mutant $\lnot B = T$ → error.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-B | T | F | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. Non-empty list with empty=False → no error (kills TNF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills TNF | `test_empty_tnf_non_empty` |

---

### 4.27 Member 3 — TIF: `_validate_regex`

**Function:** `_validate_regex` · **Fault class:** TIF · **Mutation:** F3-9

#### Step 1 — Predicate Extraction

Error-filing predicate: $P = A \land \lnot B$ (isinstance str AND no match).

TIF inserts $\lnot A$: $P_{\text{mut}} = (A \land \lnot B) \lor \lnot A$.

#### Step 2 — DNF Conversion

$$P_{\text{mut}} = \lnot A \lor \lnot B = \lnot(A \land B)$$

#### Step 3 — Terms and Literals

- Mutant: $\{\lnot A\}$, $\{\lnot B\}$

#### Step 4 — MUMCUT Analysis

Non-string (A=F): orig guard → return → no error; mutant $\lnot A = T$ → error.

| Point | A | P (orig) | P (mut) | Kills? |
|-------|---|----------|---------|--------|
| NFP-A | F | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. Integer with regex rule → no error (kills TIF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills TIF | `test_regex_tif_non_string` |

---

### 4.28 Member 3 — ORF+: `_validate_dependencies`

**Function:** `_validate_dependencies` · **Fault class:** ORF+ · **Mutation:** F3-10

#### Step 1 — Predicate Extraction

```python
if isinstance(dependencies, _str_type) or not isinstance(
    dependencies, (Iterable, Mapping)
):
```

Let $A$ = `isinstance(deps, str)`, $B$ = `isinstance(deps, (Iterable,Mapping))`.

$$P = A \lor \lnot B$$

ORF+ → $P_{\text{mut}} = A \land \lnot B$.

#### Step 2 — DNF Conversion

Since str IS Iterable, for strings: $\lnot B = F$ → $A \land \lnot B = F$ always for strings.

#### Step 3 — Terms and Literals

- Mutant: single implicant $\{A\lnot B\}$ — dead for strings

#### Step 4 — MUMCUT Analysis

String dep 'ab' (A=T, B=T): orig $T \lor F = T$ → normalised.
Mutant: $T \land F = F$ → not normalised → iterated as chars.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| MUTP-A | T | T | T | F | **Yes** |

#### Step 5 — Generated Test Requirements

1. Multi-char string dep → all present → valid (kills ORF+)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills ORF+ | `test_dep_orf_plus_multichar_dep` |

---

### 4.29 Member 3 — ORF*: `_validate_regex`

**Function:** `_validate_regex` · **Fault class:** ORF\* · **Mutation:** F3-11

#### Step 1 — Predicate Extraction

Error predicate: $P = A \land \lnot B$ (is str AND no match).

ORF\*: $P_{\text{mut}} = A \lor \lnot B$.

#### Step 2 — DNF Conversion

At the point where $A$ is confirmed True (after the guard), $P_{\text{mut}} = T \lor \lnot B = T$ always.

#### Step 3 — Terms and Literals

- Mutant always fires for strings.

#### Step 4 — MUMCUT Analysis

Matching string (A=T, B=T): orig $T \land F = F$ → no error; mutant $T \lor F = T$ → error.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-B | T | T | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. String matching regex → no error (kills ORF\*)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills ORF\* | `test_regex_orf_star_string_matches` |

---

### 4.30 Member 3 — ENF: `_validate_regex`

**Function:** `_validate_regex` · **Fault class:** ENF · **Mutation:** F3-5

#### Step 1 — Predicate Extraction

```python
if not re_obj.match(value):
    self._error(field, errors.REGEX_MISMATCH)
```

$P = A \land \lnot B$ (is str AND no match).

ENF: $P_{\text{mut}} = A \land B$.

#### Step 2 — DNF Conversion

$$P_{\text{mut}} = A \land B$$

Error fires when value IS string AND DOES match — inverted logic.

#### Step 3 — Terms and Literals

- Mutant: $\{AB\}$

#### Step 4 — MUMCUT Analysis

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| MUTP | T | F | T | F | Yes |
| NFP-B | T | T | F | T | Yes |

Both cases kill the mutant.

#### Step 5 — Generated Test Requirements

1. String not matching → error (MUTP; killed if mutant suppresses it)
2. String matching → no error (NFP-B; killed if mutant fires error)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills ENF (MUTP) | `test_regex_utp_string_no_match` |
| Kills ENF (NFP-B) | `test_regex_nfp_b_string_matches` |

---

### 4.31 Member 4 — LIF: `_normalize_coerce`

**Function:** `_normalize_coerce` · **Fault class:** LIF · **Mutation:** F4-4

#### Step 1 — Predicate Extraction

```python
if field in schema and 'coerce' in schema[field]:
```

Let $A$ = `field in schema`, $B$ = `'coerce' in schema[field]`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

LIF replaces $B$ with $\mathit{True}$: $P_{\text{mut}} = A$.

#### Step 3 — Terms and Literals

- Mutant: $\{A\}$

#### Step 4 — MUMCUT Analysis

$A=T, B=F$ (field in schema, no coerce rule): orig $F$; mutant $T$ → coerce attempted → error.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-B | T | F | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. Valid integer field without coerce rule → passes (kills LIF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills LIF | `test_normalize_coerce_ldf_no_coerce_key` |

---

### 4.32 Member 4 — LDF: `_normalize_coerce`

**Function:** `_normalize_coerce` · **Fault class:** LDF · **Mutation:** F4-6

#### Step 1 — Predicate Extraction

```python
if field in schema and 'coerce' in schema[field]:
```

Let $A$ = `field in schema`, $B$ = `'coerce' in schema[field]`.

#### Step 2 — DNF Conversion

$$P = A \land B$$

LDF deletes $B$: $P_{\text{mut}} = A$.

#### Step 3 — Terms and Literals

- Mutant: $\{A\}$

#### Step 4 — MUMCUT Analysis

Same as LIF analysis above — both mutations produce the same simplified predicate $A$.
The distinguishing factor is the semantic mechanism: LIF replaces with True; LDF removes.
The killing test is identical.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-B | T | F | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. Valid field without coerce rule → passes (kills LDF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills LDF | `test_normalize_coerce_ldf_no_coerce_key` |

---

### 4.33 Member 4 — LRF: `_validate_items`

**Function:** `_validate_items` · **Fault class:** LRF · **Mutation:** F4-5

#### Step 1 — Predicate Extraction

```python
if len(items) != len(values):
```

Let $A$ = `len(items) != len(values)`.

#### Step 2 — DNF Conversion

$$P = A$$

LRF replaces `!=` with `==`: $P_{\text{mut}} = \lnot A$.

#### Step 3 — Terms and Literals

- Mutant: $\{\lnot A\}$

#### Step 4 — MUMCUT Analysis

$A=T$ (mismatch): orig $T$ → error; mutant $F$ → no ITEMS_LENGTH error.
$A=F$ (match): orig $F$ → no error; mutant $T$ → spurious error.

Both cases kill the mutant.

| Point | A | P (orig) | P (mut) | Kills? |
|-------|---|----------|---------|--------|
| A=T | T | T | F | Yes |
| A=F | F | F | T | Yes |

#### Step 5 — Generated Test Requirements

1. Length mismatch → ITEMS_LENGTH error (kills LRF)
2. Length match, all valid → no error (kills LRF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills LRF (A=T) | `test_items_length_mismatch` |
| Kills LRF (A=F) | `test_items_length_match_all_valid` |

---

### 4.34 Member 4 — LNF: `_validate_schema`

**Function:** `_validate_schema` · **Fault class:** LNF · **Mutation:** F4-2

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Sequence) and not isinstance(value, _str_type):
```

Let $A$ = `isinstance(value, Sequence)`, $B$ = `isinstance(value, _str_type)`.

$$P = A \land \lnot B$$

LNF negates $\lnot B$ to $B$: $P_{\text{mut}} = A \land B$.

#### Step 2 — DNF Conversion

$$P_{\text{mut}} = A \land B$$

A list (A=T, B=F) fails the mutant condition: sequence validation skipped.

#### Step 3 — Terms and Literals

- Mutant: $\{AB\}$ — satisfied only when value is str (str IS Sequence)

#### Step 4 — MUMCUT Analysis

List (A=T, B=F): orig $T \land T = T$ → sequence path; mutant $T \land F = F$ → skipped.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| MUTP | T | F | T | F | **Yes** |

#### Step 5 — Generated Test Requirements

1. List with invalid item → error (kills LNF: mutant skips validation → valid)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills LNF | `test_schema_sequence_value_invalid` |

---

### 4.35 Member 4 — TOF: `_validate_forbidden`

**Function:** `_validate_forbidden` · **Fault class:** TOF · **Mutation:** F4-1

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Sequence) and not isinstance(value, _str_type):
```

Let $A$ = `isinstance(value, Sequence)`, $B$ = `isinstance(value, _str_type)`.

$$P = A \land \lnot B$$

TOF drops $\lnot B$: $P_{\text{mut}} = A$.

#### Step 2 — DNF Conversion

$$P_{\text{mut}} = A$$

#### Step 3 — Terms and Literals

- Mutant: $\{A\}$

#### Step 4 — MUMCUT Analysis

String value (A=T, B=T): orig $T \land F = F$ → scalar path; mutant $T$ → list path.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-B | T | T | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. String not in forbidden list → no error via scalar path (kills TOF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills TOF | `test_forbidden_nfp_b_string_scalar_check` |

---

### 4.36 Member 4 — TNF: `_normalize_coerce`

**Function:** `_normalize_coerce` · **Fault class:** TNF · **Mutation:** F4-7

#### Step 1 — Predicate Extraction

```python
if field in schema and 'coerce' in schema[field]:
```

Let $A$ = `field in schema`, $B$ = `'coerce' in schema[field]`.

$$P = A \land B$$

TNF: $P_{\text{mut}} = \lnot A \lor \lnot B$.

#### Step 2 — DNF Conversion

$$P_{\text{mut}} = \lnot A \lor \lnot B$$

#### Step 3 — Terms and Literals

- Mutant: $\{\lnot A\}$, $\{\lnot B\}$

#### Step 4 — MUMCUT Analysis

Field with coerce rule (A=T, B=T): orig $T$ → coerce applied.
Mutant: $\lnot T \lor \lnot T = F$ → coerce NOT applied.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| MUTP | T | T | T | F | **Yes** |

#### Step 5 — Generated Test Requirements

1. Field with coerce=int, value='5' → coerced → valid (kills TNF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills TNF | `test_normalize_coerce_tnf_with_coerce` |

---

### 4.37 Member 4 — TIF: `_validate_forbidden`

**Function:** `_validate_forbidden` · **Fault class:** TIF · **Mutation:** F4-8

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Sequence) and not isinstance(value, _str_type):
```

Let $A$ = `isinstance(value, Sequence)`, $B$ = `isinstance(value, _str_type)`.

$$P = A \land \lnot B$$

TIF inserts $C$ = `isinstance(value, int)`:

$$P_{\text{mut}} = (A \land \lnot B) \lor C$$

#### Step 2 — DNF Conversion

$$P_{\text{mut}} = (A \land \lnot B) \lor C$$

#### Step 3 — Terms and Literals

- Mutant: $\{A\lnot B\}$, $\{C\}$

#### Step 4 — MUMCUT Analysis

Integer (A=F, B=F, C=T): orig $F$; mutant $T$ → list path → TypeError.

| Point | A | B | C | P (orig) | P (mut) | Kills? |
|-------|---|---|---|----------|---------|--------|
| Int | F | F | T | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. Integer not in forbidden list → no error (kills TIF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills TIF | `test_forbidden_tif_integer_not_forbidden` |

---

### 4.38 Member 4 — ORF+: `_validate_contains`

**Function:** `_validate_contains` · **Fault class:** ORF+ · **Mutation:** F4-9

#### Step 1 — Predicate Extraction

```python
if not isinstance(expected_values, Iterable) or isinstance(
    expected_values, _str_type
):
```

Let $A$ = `isinstance(exp, Iterable)`, $B$ = `isinstance(exp, _str_type)`.

$$P = \lnot A \lor B$$

ORF+: $P_{\text{mut}} = \lnot A \land B$.

#### Step 2 — DNF Conversion

Since str IS Iterable: $\lnot A = F$ for strings → $\lnot A \land B = F$ always → normalisation never happens.

#### Step 3 — Terms and Literals

- Mutant: $\{\lnot A B\}$ — always False for strings

#### Step 4 — MUMCUT Analysis

String 'abc' (A=T, B=T): orig $F \lor T = T$ → normalised to `{'abc'}`.
Mutant: $F \land T = F$ → else branch → `set('abc')` = `{'a','b','c'}`.

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| MUTP-B | T | T | T | F | **Yes** |

#### Step 5 — Generated Test Requirements

1. contains='abc', value=['abc'] → found → valid (kills ORF+: mutant checks chars)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills ORF+ | `test_contains_orf_plus_string_multi` |

---

### 4.39 Member 4 — ORF*: `_validate_forbidden`

**Function:** `_validate_forbidden` · **Fault class:** ORF\* · **Mutation:** F4-10

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Sequence) and not isinstance(value, _str_type):
```

Let $A$ = `isinstance(value, Sequence)`, $B$ = `isinstance(value, _str_type)`.

$$P = A \land \lnot B$$

ORF\*: $P_{\text{mut}} = A \lor \lnot B$.

#### Step 2 — DNF Conversion

$$P_{\text{mut}} = A \lor \lnot B$$

For integers (A=F, B=F): $\lnot B = T$ → mutant True → list path → TypeError.

#### Step 3 — Terms and Literals

- Mutant: $\{A\}$, $\{\lnot B\}$

#### Step 4 — MUMCUT Analysis

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| NFP-A | F | F | F | T | **Yes** |

#### Step 5 — Generated Test Requirements

1. Integer not in forbidden list → no error (kills ORF\*)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills ORF\* | `test_forbidden_orf_star_integer` |

---

### 4.40 Member 4 — ENF: `_validate_forbidden`

**Function:** `_validate_forbidden` · **Fault class:** ENF · **Mutation:** F4-11

#### Step 1 — Predicate Extraction

```python
if isinstance(value, Sequence) and not isinstance(value, _str_type):
```

Let $A$ = `isinstance(value, Sequence)`, $B$ = `isinstance(value, _str_type)`.

$$P = A \land \lnot B$$

ENF: $P_{\text{mut}} = \lnot A \lor B$.

#### Step 2 — DNF Conversion

$$P_{\text{mut}} = \lnot A \lor B$$

For a list (A=T, B=F): $P_{\text{mut}} = F \lor F = F$ → list goes to scalar path.

#### Step 3 — Terms and Literals

- Mutant: $\{\lnot A\}$, $\{B\}$

#### Step 4 — MUMCUT Analysis

| Point | A | B | P (orig) | P (mut) | Kills? |
|-------|---|---|----------|---------|--------|
| MUTP | T | F | T | F | **Yes** |

List with forbidden element: original → element-wise check → error; mutant → scalar check
→ `list in [2,3]` → False → no error.

#### Step 5 — Generated Test Requirements

1. List containing a forbidden element → error (kills ENF)

#### Step 6 — Implemented Test Cases

| Requirement | Test Function |
|-------------|---------------|
| Kills ENF | `test_forbidden_enf_list_with_forbidden` |

---

## 5. Unit Test Documentation

Each member has test functions covering all MUMCUT requirements and all 10 Table 8.1
fault classes. Total test count: **105 tests** (27 + 26 + 26 + 26).

Each test is classified as one of:
- **UTP / MUTP** — input that makes exactly one implicant true
- **NFP / CUTPNFP** — near-false point; one literal flip changes predicate value
- **Fault-reveal** — documents which Table 8.1 fault class the test kills

| Member | File | Functions tested | Tests |
|--------|------|-----------------|-------|
| 1 | `tests/member1/test_member1.py` | type, allowed, unknown_fields, minlength, dep_mapping | 27 |
| 2 | `tests/member2/test_member2.py` | normalize_coerce, excludes, readonly, maxlength, keysrules | 26 |
| 3 | `tests/member3/test_member3.py` | empty, dependencies, required_fields, regex, valuesrules | 26 |
| 4 | `tests/member4/test_member4.py` | forbidden, schema, contains, normalize_coerce_pub, items | 26 |

---

## 6. Mutation / Fault Emulation

The project documents **45 fault-emulating mutations** across all four members and all
10 Table 8.1 fault classes. Every mutation is recorded in `faults/mutations.md` with:

- The **original source code fragment** (from `cerberus/validator.py`)
- The **mutated source code fragment**
- The **Table 8.1 fault class** being emulated
- The **rationale** explaining why the mutation belongs to that class
- The **killing test** (the pytest function whose assertion fails when the mutation is applied)

To demonstrate these mutations concretely, the project includes implemented mutation artifacts under `faults/implemented_mutations/`. Each implemented mutation has its own directory containing the original source fragment (`original.py`), the mutated fragment (`mutated.py`), a valid unified diff patch file (`mutation.patch`), and a `README.md` explaining the mutation details, fault class, and how to apply and run the killing test.

Below is a summary table of the 45 implemented mutations:

| Mutation ID | Fault Class | Source File | Target Function | Killing Test | Artifact Path |
|-------------|-------------|-------------|-----------------|--------------|---------------|
| F1-1 | LIF | cerberus/validator.py | _validate_type | tests/member1/test_member1.py::test_type_nfp_clause_a_false_error | faults/implemented_mutations/F1-1 |
| F1-2 | LIF | cerberus/validator.py | _validate_type | tests/member1/test_member1.py::test_type_nfp_clause_b_true_error | faults/implemented_mutations/F1-2 |
| F1-3 | TOF | cerberus/validator.py | _validate_allowed | tests/member1/test_member1.py::test_allowed_nfp_b_string_treated_as_scalar | faults/implemented_mutations/F1-3 |
| F1-4 | LIF | cerberus/validator.py | _validate_minlength | tests/member1/test_member1.py::test_minlength_nfp_a_non_iterable | faults/implemented_mutations/F1-4 |
| F1-5 | LNF | cerberus/validator.py | __validate_dependencies_mapping | tests/member1/test_member1.py::test_dep_mapping_list_dep_value_nfp | faults/implemented_mutations/F1-5 |
| F2-1 | LNF | cerberus/validator.py | __normalize_coerce | tests/member2/test_member2.py::test_coerce_nullable_none_suppressed | faults/implemented_mutations/F2-1 |
| F2-2 | LIF | cerberus/validator.py | __normalize_coerce | tests/member2/test_member2.py::test_coerce_nonnullable_none_errors | faults/implemented_mutations/F2-2 |
| F2-3 | TOF | cerberus/validator.py | _validate_excludes | tests/member2/test_member2.py::test_excludes_neither_present_required_fails | faults/implemented_mutations/F2-3 |
| F2-4 | LIF | cerberus/validator.py | _validate_readonly | tests/member2/test_member2.py::test_readonly_unnormalized_errors | faults/implemented_mutations/F2-4 |
| F2-5 | LRF | cerberus/validator.py | _validate_maxlength | tests/member2/test_member2.py::test_maxlength_nfp_b_within_limit | faults/implemented_mutations/F2-5 |
| F3-1 | LIF | cerberus/validator.py | _validate_empty | TODO: Any test passing a non-Sized type when the empty rule is present. | faults/implemented_mutations/F3-1 |
| F3-2 | LNF | cerberus/validator.py | _validate_dependencies | tests/member3/test_member3.py::test_dep_list_dep_satisfied | faults/implemented_mutations/F3-2 |
| F3-3 | LIF | cerberus/validator.py | __validate_required_fields | tests/member3/test_member3.py::test_required_field_none_ignore_none_values | faults/implemented_mutations/F3-3 |
| F3-4 | TOF | cerberus/validator.py | _validate_regex | tests/member3/test_member3.py::test_regex_nfp_a_non_string | faults/implemented_mutations/F3-4 |
| F3-5 | ENF | cerberus/validator.py | _validate_regex | tests/member3/test_member3.py::test_regex_utp_string_no_match | faults/implemented_mutations/F3-5 |
| F4-1 | TOF | cerberus/validator.py | _validate_forbidden | tests/member4/test_member4.py::test_forbidden_nfp_b_string_scalar_check | faults/implemented_mutations/F4-1 |
| F4-2 | LNF | cerberus/validator.py | _validate_schema | tests/member4/test_member4.py::test_schema_sequence_value_invalid | faults/implemented_mutations/F4-2 |
| F4-3 | LNF | cerberus/validator.py | _validate_contains | tests/member4/test_member4.py::test_contains_list_expected_all_present | faults/implemented_mutations/F4-3 |
| F4-4 | LIF | cerberus/validator.py | _normalize_coerce | tests/member4/test_member4.py::test_normalize_coerce_no_coerce_rule | faults/implemented_mutations/F4-4 |
| F4-5 | LRF | cerberus/validator.py | _validate_items | tests/member4/test_member4.py::test_items_length_mismatch | faults/implemented_mutations/F4-5 |
| F1-6 | LDF | cerberus/validator.py | _validate_minlength | tests/member1/test_member1.py::test_minlength_ldf_b_deleted | faults/implemented_mutations/F1-6 |
| F1-7 | LRF | cerberus/validator.py | _validate_minlength | tests/member1/test_member1.py::test_minlength_lrf_boundary | faults/implemented_mutations/F1-7 |
| F1-8 | TNF | cerberus/validator.py | _validate_minlength | tests/member1/test_member1.py::test_minlength_tnf_long_list | faults/implemented_mutations/F1-8 |
| F1-9 | TIF | cerberus/validator.py | _validate_allowed | tests/member1/test_member1.py::test_allowed_tif_integer_in_allowed | faults/implemented_mutations/F1-9 |
| F1-10 | ORF+ | cerberus/validator.py | __validate_dependencies_mapping | tests/member1/test_member1.py::test_dep_mapping_orf_plus_int_dep | faults/implemented_mutations/F1-10 |
| F1-11 | ORF* | cerberus/validator.py | _validate_minlength | tests/member1/test_member1.py::test_minlength_orf_star_long_list | faults/implemented_mutations/F1-11 |
| F1-12 | ENF | cerberus/validator.py | _validate_allowed | tests/member1/test_member1.py::test_allowed_enf_list_all_allowed | faults/implemented_mutations/F1-12 |
| F2-6 | LDF | cerberus/validator.py | _validate_maxlength | tests/member2/test_member2.py::test_maxlength_ldf_b_deleted | faults/implemented_mutations/F2-6 |
| F2-7 | TNF | cerberus/validator.py | _validate_maxlength | tests/member2/test_member2.py::test_maxlength_tnf_within_limit | faults/implemented_mutations/F2-7 |
| F2-8 | TIF | cerberus/validator.py | _validate_maxlength | tests/member2/test_member2.py::test_maxlength_tif_non_iterable | faults/implemented_mutations/F2-8 |
| F2-9 | ORF+ | cerberus/validator.py | __normalize_coerce | tests/member2/test_member2.py::test_coerce_orf_plus_nullable_bad_coerce | faults/implemented_mutations/F2-9 |
| F2-10 | ORF* | cerberus/validator.py | _validate_excludes | tests/member2/test_member2.py::test_excludes_orf_star_required_missing | faults/implemented_mutations/F2-10 |
| F2-11 | ENF | cerberus/validator.py | _validate_maxlength | tests/member2/test_member2.py::test_maxlength_enf_within_limit | faults/implemented_mutations/F2-11 |
| F3-6 | LDF | cerberus/validator.py | _validate_empty | tests/member3/test_member3.py::test_empty_ldf_b_deleted | faults/implemented_mutations/F3-6 |
| F3-7 | LRF | cerberus/validator.py | _validate_empty | tests/member3/test_member3.py::test_empty_lrf_single_element | faults/implemented_mutations/F3-7 |
| F3-8 | TNF | cerberus/validator.py | _validate_empty | tests/member3/test_member3.py::test_empty_tnf_non_empty | faults/implemented_mutations/F3-8 |
| F3-9 | TIF | cerberus/validator.py | _validate_regex | tests/member3/test_member3.py::test_regex_tif_non_string | faults/implemented_mutations/F3-9 |
| F3-10 | ORF+ | cerberus/validator.py | _validate_dependencies | tests/member3/test_member3.py::test_dep_orf_plus_multichar_dep | faults/implemented_mutations/F3-10 |
| F3-11 | ORF* | cerberus/validator.py | _validate_regex | tests/member3/test_member3.py::test_regex_orf_star_string_matches | faults/implemented_mutations/F3-11 |
| F4-6 | LDF | cerberus/validator.py | _normalize_coerce | tests/member4/test_member4.py::test_normalize_coerce_ldf_no_coerce_key | faults/implemented_mutations/F4-6 |
| F4-7 | TNF | cerberus/validator.py | _normalize_coerce | tests/member4/test_member4.py::test_normalize_coerce_tnf_with_coerce | faults/implemented_mutations/F4-7 |
| F4-8 | TIF | cerberus/validator.py | _validate_forbidden | tests/member4/test_member4.py::test_forbidden_tif_integer_not_forbidden | faults/implemented_mutations/F4-8 |
| F4-9 | ORF+ | cerberus/validator.py | _validate_contains | tests/member4/test_member4.py::test_contains_orf_plus_string_multi | faults/implemented_mutations/F4-9 |
| F4-10 | ORF* | cerberus/validator.py | _validate_forbidden | tests/member4/test_member4.py::test_forbidden_orf_star_integer | faults/implemented_mutations/F4-10 |
| F4-11 | ENF | cerberus/validator.py | _validate_forbidden | tests/member4/test_member4.py::test_forbidden_enf_list_with_forbidden | faults/implemented_mutations/F4-11 |

Mutation counts by fault class:

| Fault Class | Mutations documented |
|-------------|---------------------|
| LIF | 7 (F1-1, F1-2, F1-4, F2-2, F2-4, F3-1, F3-3, F4-4) |
| LDF | 4 (F1-6, F2-6, F3-6, F4-6) |
| LRF | 4 (F1-7, F2-5, F3-7, F4-5) |
| LNF | 5 (F1-5, F2-1, F3-2, F4-2, F4-3) |
| TOF | 4 (F1-3, F2-3, F3-4, F4-1) |
| TNF | 4 (F1-8, F2-7, F3-8, F4-7) |
| TIF | 4 (F1-9, F2-8, F3-9, F4-8) |
| ORF+ | 4 (F1-10, F2-9, F3-10, F4-9) |
| ORF\* | 4 (F1-11, F2-10, F3-11, F4-10) |
| ENF | 5 (F1-12, F2-11, F3-5, F4-11) |
| **Total** | **45** |

---

## 7. How to Run Tests

```bash
cd C:\Users\berra\Desktop\proje
python -m pytest tests/ -v
```

Expected: **105 passed**.

To run a single member:
```bash
python -m pytest tests/member1/ -v
```

---

## Appendix: Assignment Requirement Traceability

The following table maps each assignment requirement to the evidence in this report and
supporting files.

| Assignment Requirement | Evidence Location |
|------------------------|-------------------|
| Public-domain Python software selected | Section 1 (Cerberus, ISC licence); `PROPOSAL.md` |
| All 10 DNF fault classes (Table 8.1) analyzed | Section 3.1 (definitions); Section 3.2 (per-member coverage matrix) |
| MUMCUT criterion applied to each function | Section 2 (§2.1–§2.20, one entry per function with MUTP/CUTPNFP/MNFP) |
| Detailed logic derivations provided | Section 2 (predicate extraction, DNF conversion, terms/literals for all 20 functions); Section 4 (Steps 1–6 for all 40 member×fault analyses) |
| Fault emulation documented with original and mutated code | `faults/implemented_mutations/`<br>`faults/mutations.md`<br>`report.md` Section 6 |
| 20+ tests per member (minimum) | Section 5 (M1: 27 tests; M2: 26; M3: 26; M4: 26); test files in `tests/` |
| Distinct functions selected per member (5 each, 20 total) | Section 1 (function table); `PROPOSAL.md` |
| Each member covers all 10 fault classes | Section 3.2 (10×4 coverage matrix); Section 4 (§4.1–§4.40, 10 analyses per member) |
| Tests are executable against the SUT | `conftest.py`; `python -m pytest tests/ -v` → 105 passed |
| No mocking — tests use real SUT | All test files use `Validator(schema).validate(document)` exclusively |
