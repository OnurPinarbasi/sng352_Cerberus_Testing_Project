# CerberusTesting – Project Report

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

## 2. DNF Fault Class Analyses

### Fault Class: LIF (Ahmet Kerem Ince (Member 1) - `_validate_type`)

#### Function Under Test
`_validate_type` in `cerberus/validator.py`

#### Mutation
F1-1: LIF mutation applied to `_validate_type`.

#### Predicate
$$
P = A \land \lnot B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land \lnot B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = \mathit{True} \land \lnot B = \lnot B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B, NFP-A is the killing test: $A=F$ means wrong type; original → error; mutant → no error.
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| MUTP-1 | `isinstance(value, included)=T, isinstance(value, excluded)=F` → no error |
| NFP-A | `isinstance(value, included)=F` → error (kills LIF on A) |
| NFP-B | value in both → error |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_type_utp_both_clauses_true_no_error | UTP: value is int (included), not excluded → valid. | Valid (True) |
| test_type_nfp_clause_a_false_error | NFP(A): value not an int → included_types check fails → type error. | Invalid (False) |
| test_type_nfp_clause_b_true_error | NFP(B): value matches included_types but also matches excluded_types → type error. | Invalid (False) |

#### Fault Detection Rationale
The mutation F1-1 simulates a LIF on `_validate_type` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LIF (Berrak Yildirim (Member 2) - `__normalize_coerce`)

#### Function Under Test
`__normalize_coerce` in `cerberus/validator.py`

#### Mutation
F2-2: LIF mutation applied to `__normalize_coerce`.

#### Predicate
$$
P = \lnot A \lor \lnot B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = \lnot A \lor \lnot B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = \lnot \mathit{True} \lor \lnot B = \lnot B
$$

#### MUMCUT Analysis
* UTP: MUTP-¬A
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | nullable=False, value=None → error (kills LIF on A) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_coerce_nonnullable_none_errors | ¬A=T (nullable=False), value=None → coerce exception not suppressed → error. | Invalid (False) |

#### Fault Detection Rationale
The mutation F2-2 simulates a LIF on `__normalize_coerce` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LIF (Onur Pinarbasi (Member 3) - `_validate_empty`)

#### Function Under Test
`_validate_empty` in `cerberus/validator.py`

#### Mutation
F3-1: LIF mutation applied to `_validate_empty`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P = A \land B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Non-Sized value with empty rule → no check (kills LIF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_empty_utp_empty_list_allowed (indirectly); key test: non-Sized via test_minlength_nfp_a_non_iterable pattern | Verifies rule validation behaviour. | Valid (True) |

#### Fault Detection Rationale
The mutation F3-1 simulates a LIF on `_validate_empty` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LIF (Zeynep Orman (Member 4) - `_normalize_coerce`)

#### Function Under Test
`_normalize_coerce` in `cerberus/validator.py`

#### Mutation
F4-4: LIF mutation applied to `_normalize_coerce`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P = A \land B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Valid integer field without coerce rule → passes (kills LIF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_normalize_coerce_ldf_no_coerce_key | LDF(B): integer field with no coerce rule is valid; mutation drops coerce-key check | Valid (True) |

#### Fault Detection Rationale
The mutation F4-4 simulates a LIF on `_normalize_coerce` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LDF (Ahmet Kerem Ince (Member 1) - `_validate_minlength`)

#### Function Under Test
`_validate_minlength` in `cerberus/validator.py`

#### Mutation
F1-6: LDF mutation applied to `_validate_minlength`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B, NFP-B is the killing test: value is Iterable but meets min_length; original → no error;
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| MUTP-1 | list too short → error |
| NFP-A | non-Iterable → no error |
| NFP-B | list of exactly min_length → no error (kills LDF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_minlength_utp_list_too_short | UTP: both clauses true → minlength error. | Invalid (False) |
| test_minlength_nfp_a_non_iterable | NFP(A): integer not Iterable → no minlength check. | Invalid (False) |
| test_minlength_ldf_b_deleted | LDF(B): list of exactly min_length is valid; mutation drops len-check → error. | Valid (True) |

#### Fault Detection Rationale
The mutation F1-6 simulates a LDF on `_validate_minlength` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LDF (Berrak Yildirim (Member 2) - `_validate_maxlength`)

#### Function Under Test
`_validate_maxlength` in `cerberus/validator.py`

#### Mutation
F2-6: LDF mutation applied to `_validate_maxlength`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | List within max_length → no error (kills LDF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_maxlength_ldf_b_deleted | LDF(B): list within limit is valid; mutation drops len-check → error. | Valid (True) |

#### Fault Detection Rationale
The mutation F2-6 simulates a LDF on `_validate_maxlength` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LDF (Onur Pinarbasi (Member 3) - `_validate_empty`)

#### Function Under Test
`_validate_empty` in `cerberus/validator.py`

#### Mutation
F3-6: LDF mutation applied to `_validate_empty`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P = A \land B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Non-empty list with empty=False → no error (kills LDF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_empty_ldf_b_deleted | LDF(B): non-empty list with empty=False is valid; mutation drops len-check → error. | Valid (True) |

#### Fault Detection Rationale
The mutation F3-6 simulates a LDF on `_validate_empty` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LDF (Zeynep Orman (Member 4) - `_normalize_coerce`)

#### Function Under Test
`_normalize_coerce` in `cerberus/validator.py`

#### Mutation
F4-6: LDF mutation applied to `_normalize_coerce`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P = A \land B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Valid field without coerce rule → passes (kills LDF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_normalize_coerce_ldf_no_coerce_key | LDF(B): integer field with no coerce rule is valid; mutation drops coerce-key check | Valid (True) |

#### Fault Detection Rationale
The mutation F4-6 simulates a LDF on `_normalize_coerce` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LRF (Ahmet Kerem Ince (Member 1) - `_validate_minlength`)

#### Function Under Test
`_validate_minlength` in `cerberus/validator.py`

#### Mutation
F1-7: LRF mutation applied to `_validate_minlength`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A \land (len(value) \leq min\_length)
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: Boundary
* CUTPNFP: Boundary

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| MUTP-1 | list with len < min → error |
| Boundary | list with len == min → no error originally, error with mutation (kills LRF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_minlength_utp_list_too_short | UTP: both clauses true → minlength error. | Invalid (False) |
| test_minlength_lrf_boundary | LRF: len == min_length is valid; mutation (<=) causes false error. | Valid (True) |

#### Fault Detection Rationale
The mutation F1-7 simulates a LRF on `_validate_minlength` by altering its logical predicate. The test case representing the Boundary condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LRF (Berrak Yildirim (Member 2) - `_validate_maxlength`)

#### Function Under Test
`_validate_maxlength` in `cerberus/validator.py`

#### Mutation
F2-5: LRF mutation applied to `_validate_maxlength`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A \land (len(value) \geq max\_length)
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: Boundary
* CUTPNFP: Boundary

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | List of exactly max_length → no error originally (kills LRF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_maxlength_nfp_b_within_limit | NFP(B): list within limit → valid. | Valid (True) |

#### Fault Detection Rationale
The mutation F2-5 simulates a LRF on `_validate_maxlength` by altering its logical predicate. The test case representing the Boundary condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LRF (Onur Pinarbasi (Member 3) - `_validate_empty`)

#### Function Under Test
`_validate_empty` in `cerberus/validator.py`

#### Mutation
F3-7: LRF mutation applied to `_validate_empty`.

#### Predicate
$$
P_{\text{mut}} = A \land (len(value) == 1)
$$

#### DNF Derivation
$$
P_{\text{orig}} = P_{\text{mut}} = A \land (len(value) == 1)
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A \land (len(value) == 1)
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Single-element list with empty=False → no error (kills LRF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_empty_lrf_single_element | LRF: single-element list is not empty → valid; mutation (==1) fires for len-1 → error. | Valid (True) |

#### Fault Detection Rationale
The mutation F3-7 simulates a LRF on `_validate_empty` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LRF (Zeynep Orman (Member 4) - `_validate_items`)

#### Function Under Test
`_validate_items` in `cerberus/validator.py`

#### Mutation
F4-5: LRF mutation applied to `_validate_items`.

#### Predicate
$$
P = A
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A
$$
$$
P_{\text{mut}} = P = A
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Length mismatch → ITEMS_LENGTH error (kills LRF) |
| Requirement | Length match, all valid → no error (kills LRF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_items_length_mismatch | p1 true: items count != values count → ITEMS_LENGTH error. | Invalid (False) |
| test_items_length_match_all_valid | p1 false, p2 false: lengths match, all items valid → valid. | Valid (True) |

#### Fault Detection Rationale
The mutation F4-5 simulates a LRF on `_validate_items` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LNF (Ahmet Kerem Ince (Member 1) - `__validate_dependencies_mapping`)

#### Function Under Test
`__validate_dependencies_mapping` in `cerberus/validator.py`

#### Mutation
F1-5: LNF mutation applied to `__validate_dependencies_mapping`.

#### Predicate
$$
P = \lnot A \lor B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = \lnot A \lor B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A \lor B
$$

#### MUMCUT Analysis
* UTP: MUTP-¬A, MUTP-B, MUTP-¬A differs: original True, mutant False → **kills mutant**.
* NFP: NFP-¬A, NFP-B
* CUTPNFP: NFP-¬A, NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| MUTP-¬A | scalar dep value → normalised to list → dep satisfied (kills LNF) |
| MUTP-B | string dep value → normalised |
| NFP | list dep value → used directly (predicate false) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_dep_mapping_scalar_dep_value_satisfied | dep_value is int (not Sequence) → normalised; dependency satisfied → valid. | Valid (True) |
| test_dep_mapping_string_dep_value_satisfied | dep_value is str → normalised to list; dependency satisfied → valid. | Valid (True) |
| test_dep_mapping_list_dep_value_nfp | NFP: dep_values is list → predicate false → used directly; mismatch → error. | Invalid (False) |

#### Fault Detection Rationale
The mutation F1-5 simulates a LNF on `__validate_dependencies_mapping` by altering its logical predicate. The test case representing the NFP-¬A, NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LNF (Berrak Yildirim (Member 2) - `__normalize_coerce`)

#### Function Under Test
`__normalize_coerce` in `cerberus/validator.py`

#### Mutation
F2-1: LNF mutation applied to `__normalize_coerce`.

#### Predicate
$$
P_{\text{mut}} = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P_{\text{mut}} = A \land B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A \land B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | nullable=True, value=None → no error (kills LNF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_coerce_nullable_none_suppressed | NFP: A∧B → p=False → exception suppressed → no coerce error. | Invalid (False) |

#### Fault Detection Rationale
The mutation F2-1 simulates a LNF on `__normalize_coerce` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LNF (Onur Pinarbasi (Member 3) - `_validate_dependencies`)

#### Function Under Test
`_validate_dependencies` in `cerberus/validator.py`

#### Mutation
F3-2: LNF mutation applied to `_validate_dependencies`.

#### Predicate
$$
P_{\text{mut}} = A \lor B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P_{\text{mut}} = A \lor B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A \lor B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | List deps → used directly (kills LNF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_dep_list_dep_satisfied | NFP: deps is list (A=F,B=T) → used directly → all deps present → valid. | Valid (True) |

#### Fault Detection Rationale
The mutation F3-2 simulates a LNF on `_validate_dependencies` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: LNF (Zeynep Orman (Member 4) - `_validate_schema`)

#### Function Under Test
`_validate_schema` in `cerberus/validator.py`

#### Mutation
F4-2: LNF mutation applied to `_validate_schema`.

#### Predicate
$$
P_{\text{mut}} = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P_{\text{mut}} = A \land B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A \land B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| List with invalid item → error (kills LNF | mutant skips validation → valid) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_schema_sequence_value_invalid | value is list → sequence path → item fails schema → error. | Invalid (False) |

#### Fault Detection Rationale
The mutation F4-2 simulates a LNF on `_validate_schema` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: TOF (Ahmet Kerem Ince (Member 1) - `_validate_allowed`)

#### Function Under Test
`_validate_allowed` in `cerberus/validator.py`

#### Mutation
F1-3: TOF mutation applied to `_validate_allowed`.

#### Predicate
$$
P = A \land \lnot B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land \lnot B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B (kills), NFP-B is the killing test: string value; original → scalar path; mutant → list path.
* CUTPNFP: NFP-B (kills)

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| MUTP-1 | list value → list check path |
| NFP-B | string value → scalar path (kills TOF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_allowed_utp_list_all_allowed | UTP: list value, all items in allowed → valid. | Valid (True) |
| test_allowed_nfp_b_string_treated_as_scalar | NFP(B): string is Iterable but isinstance(_str_type) → scalar path → error if not in list. | Invalid (False) |

#### Fault Detection Rationale
The mutation F1-3 simulates a TOF on `_validate_allowed` by altering its logical predicate. The test case representing the NFP-B (kills) condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: TOF (Berrak Yildirim (Member 2) - `_validate_excludes`)

#### Function Under Test
`_validate_excludes` in `cerberus/validator.py`

#### Mutation
F2-3: TOF mutation applied to `_validate_excludes`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| y required, x not required, x excludes y, document={x | 1} → error (kills TOF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_excludes_neither_present_required_fails | required + excludes: neither present → required error. | Invalid (False) |

#### Fault Detection Rationale
The mutation F2-3 simulates a TOF on `_validate_excludes` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: TOF (Onur Pinarbasi (Member 3) - `_validate_regex`)

#### Function Under Test
`_validate_regex` in `cerberus/validator.py`

#### Mutation
F3-4: TOF mutation applied to `_validate_regex`.

#### Predicate
$$
P = A
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A
$$
$$
P_{\text{mut}} = P = A
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Integer with regex rule → no error (kills TOF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_regex_nfp_a_non_string | NFP(A): value is int → not _str_type → guard returns early, no error. | Valid (True) |

#### Fault Detection Rationale
The mutation F3-4 simulates a TOF on `_validate_regex` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: TOF (Zeynep Orman (Member 4) - `_validate_forbidden`)

#### Function Under Test
`_validate_forbidden` in `cerberus/validator.py`

#### Mutation
F4-1: TOF mutation applied to `_validate_forbidden`.

#### Predicate
$$
P_{\text{mut}} = A
$$

#### DNF Derivation
$$
P_{\text{orig}} = P_{\text{mut}} = A
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | String not in forbidden list → no error via scalar path (kills TOF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_forbidden_nfp_b_string_scalar_check | NFP(B): string value → scalar check (not element-wise) → not in list → valid. | Valid (True) |

#### Fault Detection Rationale
The mutation F4-1 simulates a TOF on `_validate_forbidden` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: TNF (Ahmet Kerem Ince (Member 1) - `_validate_minlength`)

#### Function Under Test
`_validate_minlength` in `cerberus/validator.py`

#### Mutation
F1-8: TNF mutation applied to `_validate_minlength`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = \lnot A \lor \lnot B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: The NFP-B point $(A=T, B=F)$: P(orig)=F, P(mut)=T (¬B = True) → kills mutant., NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Long list (A=T, B=F) | no error originally; with TNF → error (kills mutant) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_minlength_tnf_long_list | TNF: long-enough list is valid; mutation (¬A∨¬B) fires when len>=min → error. | Valid (True) |

#### Fault Detection Rationale
The mutation F1-8 simulates a TNF on `_validate_minlength` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: TNF (Berrak Yildirim (Member 2) - `_validate_maxlength`)

#### Function Under Test
`_validate_maxlength` in `cerberus/validator.py`

#### Mutation
F2-7: TNF mutation applied to `_validate_maxlength`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P = A \land B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | List within max_length → no error (kills TNF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_maxlength_tnf_within_limit | TNF: within-limit list is valid; mutation (¬A∨¬B) fires when len<=max → error. | Valid (True) |

#### Fault Detection Rationale
The mutation F2-7 simulates a TNF on `_validate_maxlength` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: TNF (Onur Pinarbasi (Member 3) - `_validate_empty`)

#### Function Under Test
`_validate_empty` in `cerberus/validator.py`

#### Mutation
F3-8: TNF mutation applied to `_validate_empty`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P = A \land B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Non-empty list with empty=False → no error (kills TNF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_empty_tnf_non_empty | TNF: non-empty list is valid; mutation (¬A∨¬B) fires when len!=0 → error. | Valid (True) |

#### Fault Detection Rationale
The mutation F3-8 simulates a TNF on `_validate_empty` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: TNF (Zeynep Orman (Member 4) - `_normalize_coerce`)

#### Function Under Test
`_normalize_coerce` in `cerberus/validator.py`

#### Mutation
F4-7: TNF mutation applied to `_normalize_coerce`.

#### Predicate
$$
P_{\text{mut}} = \lnot A \lor \lnot B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P_{\text{mut}} = \lnot A \lor \lnot B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = \lnot A \lor \lnot B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Field with coerce=int, value='5' → coerced → valid (kills TNF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_normalize_coerce_tnf_with_coerce | TNF: coerce=int converts '5' → integer → valid; mutation negates condition | Valid (True) |

#### Fault Detection Rationale
The mutation F4-7 simulates a TNF on `_normalize_coerce` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: TIF (Ahmet Kerem Ince (Member 1) - `_validate_allowed`)

#### Function Under Test
`_validate_allowed` in `cerberus/validator.py`

#### Mutation
F1-9: TIF mutation applied to `_validate_allowed`.

#### Predicate
$$
P = A \land \lnot B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land \lnot B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = (A \land \lnot B) \lor C
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Integer value in allowed list → valid via scalar path (kills TIF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_allowed_tif_integer_in_allowed | TIF: integer in allowed list is valid; mutation sends int to list path → TypeError. | Valid (True) |

#### Fault Detection Rationale
The mutation F1-9 simulates a TIF on `_validate_allowed` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: TIF (Berrak Yildirim (Member 2) - `_validate_maxlength`)

#### Function Under Test
`_validate_maxlength` in `cerberus/validator.py`

#### Mutation
F2-8: TIF mutation applied to `_validate_maxlength`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = (A \land B) \lor \lnot A
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Integer (non-Iterable) → no maxlength check (kills TIF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_maxlength_tif_non_iterable | TIF: integer bypasses maxlength check; mutation adds non-Iterable term → error. | Invalid (False) |

#### Fault Detection Rationale
The mutation F2-8 simulates a TIF on `_validate_maxlength` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: TIF (Onur Pinarbasi (Member 3) - `_validate_regex`)

#### Function Under Test
`_validate_regex` in `cerberus/validator.py`

#### Mutation
F3-9: TIF mutation applied to `_validate_regex`.

#### Predicate
$$
P_{\text{mut}} = \lnot A \lor \lnot B = \lnot(A \land B)
$$

#### DNF Derivation
$$
P_{\text{orig}} = P_{\text{mut}} = \lnot A \lor \lnot B = \lnot(A \land B)
$$
$$
P_{\text{mut}} = P_{\text{mut}} = \lnot A \lor \lnot B = \lnot(A \land B)
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Integer with regex rule → no error (kills TIF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_regex_tif_non_string | TIF: integer bypasses regex (guard exits); mutation adds ¬A term → integer errors. | Invalid (False) |

#### Fault Detection Rationale
The mutation F3-9 simulates a TIF on `_validate_regex` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: TIF (Zeynep Orman (Member 4) - `_validate_forbidden`)

#### Function Under Test
`_validate_forbidden` in `cerberus/validator.py`

#### Mutation
F4-8: TIF mutation applied to `_validate_forbidden`.

#### Predicate
$$
P_{\text{mut}} = (A \land \lnot B) \lor C
$$

#### DNF Derivation
$$
P_{\text{orig}} = P_{\text{mut}} = (A \land \lnot B) \lor C
$$
$$
P_{\text{mut}} = P_{\text{mut}} = (A \land \lnot B) \lor C
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Integer not in forbidden list → no error (kills TIF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_forbidden_tif_integer_not_forbidden | TIF: integer not in forbidden list is valid; mutation adds int term → list path | Valid (True) |

#### Fault Detection Rationale
The mutation F4-8 simulates a TIF on `_validate_forbidden` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: ORF+ (Ahmet Kerem Ince (Member 1) - `__validate_dependencies_mapping`)

#### Function Under Test
`__validate_dependencies_mapping` in `cerberus/validator.py`

#### Mutation
F1-10: ORF+ mutation applied to `__validate_dependencies_mapping`.

#### Predicate
$$
P = \lnot A \lor B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = \lnot A \lor B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = \lnot A \land B
$$

#### MUMCUT Analysis
* UTP: MUTP-¬A
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Integer dep value → normalised to list → dep satisfied (kills ORF+) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_dep_mapping_orf_plus_int_dep | ORF+: int dep value normalised to list → valid; mutation skips normalisation → TypeError. | Valid (True) |

#### Fault Detection Rationale
The mutation F1-10 simulates a ORF+ on `__validate_dependencies_mapping` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: ORF+ (Berrak Yildirim (Member 2) - `__normalize_coerce`)

#### Function Under Test
`__normalize_coerce` in `cerberus/validator.py`

#### Mutation
F2-9: ORF+ mutation applied to `__normalize_coerce`.

#### Predicate
$$
P = \lnot A \lor \lnot B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = \lnot A \lor \lnot B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = \lnot A \land \lnot B
$$

#### MUMCUT Analysis
* UTP: MUTP-¬B
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | nullable=True, bad coerce value (≠None) → error propagated (kills ORF+) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_coerce_orf_plus_nullable_bad_coerce | ORF+: nullable=True, bad coerce value → exception should propagate → error; | Invalid (False) |

#### Fault Detection Rationale
The mutation F2-9 simulates a ORF+ on `__normalize_coerce` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: ORF+ (Onur Pinarbasi (Member 3) - `_validate_dependencies`)

#### Function Under Test
`_validate_dependencies` in `cerberus/validator.py`

#### Mutation
F3-10: ORF+ mutation applied to `_validate_dependencies`.

#### Predicate
$$
P = A
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A
$$
$$
P_{\text{mut}} = P = A
$$

#### MUMCUT Analysis
* UTP: MUTP-A
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Multi-char string dep → all present → valid (kills ORF+) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_dep_orf_plus_multichar_dep | ORF+: string dep 'ab' normalised to ('ab',) → valid; mutation skips normalisation | Valid (True) |

#### Fault Detection Rationale
The mutation F3-10 simulates a ORF+ on `_validate_dependencies` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: ORF+ (Zeynep Orman (Member 4) - `_validate_contains`)

#### Function Under Test
`_validate_contains` in `cerberus/validator.py`

#### Mutation
F4-9: ORF+ mutation applied to `_validate_contains`.

#### Predicate
$$
P = A
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A
$$
$$
P_{\text{mut}} = P = A
$$

#### MUMCUT Analysis
* UTP: MUTP-B
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| contains='abc', value=['abc'] → found → valid (kills ORF+ | mutant checks chars) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_contains_orf_plus_string_multi | ORF+: contains='abc' normalised to ('abc',) → 'abc' in list → valid; | Valid (True) |

#### Fault Detection Rationale
The mutation F4-9 simulates a ORF+ on `_validate_contains` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: ORF* (Ahmet Kerem Ince (Member 1) - `_validate_minlength`)

#### Function Under Test
`_validate_minlength` in `cerberus/validator.py`

#### Mutation
F1-11: ORF* mutation applied to `_validate_minlength`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A \lor B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | List of length > min_length → no error originally (kills ORF\*) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_minlength_orf_star_long_list | ORF*: list exceeding min is valid; mutation (A∨B) fires for any Iterable → error. | Valid (True) |

#### Fault Detection Rationale
The mutation F1-11 simulates a ORF* on `_validate_minlength` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: ORF* (Berrak Yildirim (Member 2) - `_validate_excludes`)

#### Function Under Test
`_validate_excludes` in `cerberus/validator.py`

#### Mutation
F2-10: ORF* mutation applied to `_validate_excludes`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A \lor B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| y required, x not required, x excludes y, document={x | 1} → error (kills ORF\*) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_excludes_orf_star_required_missing | ORF*: required field y not exempted when non-required x excludes it; | Invalid (False) |

#### Fault Detection Rationale
The mutation F2-10 simulates a ORF* on `_validate_excludes` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: ORF* (Onur Pinarbasi (Member 3) - `_validate_regex`)

#### Function Under Test
`_validate_regex` in `cerberus/validator.py`

#### Mutation
F3-11: ORF* mutation applied to `_validate_regex`.

#### Predicate
$$
P = A
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A
$$
$$
P_{\text{mut}} = P = A
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | String matching regex → no error (kills ORF\*) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_regex_orf_star_string_matches | ORF*: matching string is valid; mutation (A∨¬B) fires when isinstance(str) is True → error. | Valid (True) |

#### Fault Detection Rationale
The mutation F3-11 simulates a ORF* on `_validate_regex` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: ORF* (Zeynep Orman (Member 4) - `_validate_forbidden`)

#### Function Under Test
`_validate_forbidden` in `cerberus/validator.py`

#### Mutation
F4-10: ORF* mutation applied to `_validate_forbidden`.

#### Predicate
$$
P_{\text{mut}} = A \lor \lnot B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P_{\text{mut}} = A \lor \lnot B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A \lor \lnot B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | Integer not in forbidden list → no error (kills ORF\*) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_forbidden_orf_star_integer | ORF*: integer not in forbidden is valid; mutation (A∨¬B) sends int to list path | Valid (True) |

#### Fault Detection Rationale
The mutation F4-10 simulates a ORF* on `_validate_forbidden` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: ENF (Ahmet Kerem Ince (Member 1) - `_validate_allowed`)

#### Function Under Test
`_validate_allowed` in `cerberus/validator.py`

#### Mutation
F1-12: ENF mutation applied to `_validate_allowed`.

#### Predicate
$$
P = A \land \lnot B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land \lnot B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = \lnot(A \land \lnot B) = \lnot A \lor B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| List with all allowed elements → valid (kills ENF | mutant goes to scalar path → error) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_allowed_enf_list_all_allowed | ENF: list of allowed elements is valid; mutation sends list to scalar check → error. | Valid (True) |

#### Fault Detection Rationale
The mutation F1-12 simulates a ENF on `_validate_allowed` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: ENF (Berrak Yildirim (Member 2) - `_validate_maxlength`)

#### Function Under Test
`_validate_maxlength` in `cerberus/validator.py`

#### Mutation
F2-11: ENF mutation applied to `_validate_maxlength`.

#### Predicate
$$
P = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P = A \land B
$$
$$
P_{\text{mut}} = P = A \land B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | List within limit → no error (kills ENF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_maxlength_enf_within_limit | ENF: within-limit list is valid; mutation negates predicate → fires for valid input. | Valid (True) |

#### Fault Detection Rationale
The mutation F2-11 simulates a ENF on `_validate_maxlength` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: ENF (Onur Pinarbasi (Member 3) - `_validate_regex`)

#### Function Under Test
`_validate_regex` in `cerberus/validator.py`

#### Mutation
F3-5: ENF mutation applied to `_validate_regex`.

#### Predicate
$$
P_{\text{mut}} = A \land B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P_{\text{mut}} = A \land B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = A \land B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-B
* CUTPNFP: NFP-B

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | String not matching → error (MUTP; killed if mutant suppresses it) |
| Requirement | String matching → no error (NFP-B; killed if mutant fires error) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_regex_utp_string_no_match | UTP: both clauses true → REGEX_MISMATCH error. | Invalid (False) |
| test_regex_nfp_b_string_matches | NFP(B): value matches regex → valid. | Valid (True) |

#### Fault Detection Rationale
The mutation F3-5 simulates a ENF on `_validate_regex` by altering its logical predicate. The test case representing the NFP-B condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

### Fault Class: ENF (Zeynep Orman (Member 4) - `_validate_forbidden`)

#### Function Under Test
`_validate_forbidden` in `cerberus/validator.py`

#### Mutation
F4-11: ENF mutation applied to `_validate_forbidden`.

#### Predicate
$$
P_{\text{mut}} = \lnot A \lor B
$$

#### DNF Derivation
$$
P_{\text{orig}} = P_{\text{mut}} = \lnot A \lor B
$$
$$
P_{\text{mut}} = P_{\text{mut}} = \lnot A \lor B
$$

#### MUMCUT Analysis
* UTP: MUTP-1
* NFP: NFP-A, NFP-B
* CUTPNFP: NFP-A

#### Test Requirements
| Requirement | Conditions |
| ----------- | ---------- |
| Requirement | List containing a forbidden element → error (kills ENF) |

#### Test Cases
| Test | Inputs | Expected Result |
| ---- | ------ | --------------- |
| test_forbidden_enf_list_with_forbidden | ENF: list [1,2] contains forbidden 2 → should error; mutation negates predicate | Invalid (False) |

#### Fault Detection Rationale
The mutation F4-11 simulates a ENF on `_validate_forbidden` by altering its logical predicate. The test case representing the NFP-A condition provides the specific input that exposes this change. While the clean implementation validates the document under this condition, the mutated version yields a conflicting result. This assertion mismatch successfully detects and kills the mutant.

---

