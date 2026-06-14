# CerberusTesting – Project Proposal

## System Under Test
**Cerberus** — Python data validation library (public domain / ISC licence).
Source: `C:\Users\berra\cerberus\`

## Objective
Apply MUMCUT (Criterion 8.30) and DNF fault-class analysis (Table 8.1) to 20 functions
selected from `cerberus/validator.py`, covering all 10 DNF fault classes via 105 pytest tests.

## Team
| Member | Functions |
|--------|-----------|
| 1 | `_validate_type`, `_validate_allowed`, `__validate_unknown_fields`, `_validate_minlength`, `__validate_dependencies_mapping` |
| 2 | `__normalize_coerce`, `_validate_excludes`, `_validate_readonly`, `_validate_maxlength`, `_validate_keysrules` |
| 3 | `_validate_empty`, `_validate_dependencies`, `__validate_required_fields`, `_validate_regex`, `_validate_valuesrules` |
| 4 | `_validate_forbidden`, `_validate_schema`, `_validate_contains`, `_normalize_coerce`, `_validate_items` |

## Methodology
1. Extract predicate from each function.
2. Convert to minimal DNF.
3. Apply MUMCUT: compute MUTP + CUTPNFP + MNFP test requirements.
4. Map each test to a DNF fault class from Table 8.1.
5. Implement tests using only `Validator(schema).validate(document)` — no mocking.
6. Document mutations in `faults/mutations.md`.

## Running Tests
```
cd C:\Users\berra\Desktop\proje
python -m pytest tests/ -v
```

## Structure
```
proje/
  PROPOSAL.md
  conftest.py          # adds cerberus to sys.path
  tests/
    member1/test_member1.py   (20 tests)
    member2/test_member2.py   (20 tests)
    member3/test_member3.py   (20 tests)
    member4/test_member4.py   (20 tests)
  faults/mutations.md
  report/report.md
```
