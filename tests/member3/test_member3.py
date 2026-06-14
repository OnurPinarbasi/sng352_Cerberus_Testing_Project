"""
Member 3 – Functions: _validate_empty, _validate_dependencies,
__validate_required_fields, _validate_regex, _validate_valuesrules

MUMCUT predicates:
  _validate_empty          : p = isinstance(value, Sized) ∧ len(value)==0
  _validate_dependencies   : p = isinstance(deps, str) ∨ ¬isinstance(deps, (Iterable,Mapping))
  __validate_required_fields: p = doc.get(field) is not None ∨ ¬ignore_none_values
  _validate_regex          : p = isinstance(value, str) ∧ ¬re_obj.match(value)
  _validate_valuesrules    : p_outer=isinstance(value,Mapping); p_inner=validator._errors
"""
import pytest
from cerberus import Validator


# ── _validate_empty ───────────────────────────────────────────────────────────
# p = isinstance(value, Sized) AND len(value) == 0
# UTP: empty list, empty=False → error
# NFP-A: integer (not Sized) → no empty check
# NFP-B: non-empty list → predicate false, no empty error

def test_empty_utp_empty_list_not_allowed():
    """UTP: both clauses true, empty=False → EMPTY_NOT_ALLOWED error."""
    v = Validator({'x': {'type': 'list', 'empty': False}})
    assert v.validate({'x': []}) is False

def test_empty_utp_empty_list_allowed():
    """UTP: empty list, empty=True (default) → valid."""
    v = Validator({'x': {'type': 'list', 'empty': True}})
    assert v.validate({'x': []}) is True

def test_empty_nfp_b_non_empty_list():
    """NFP(B): list has items → len>0 → predicate false → no empty check."""
    v = Validator({'x': {'type': 'list', 'empty': False}})
    assert v.validate({'x': [1]}) is True

def test_empty_string_empty_not_allowed():
    """String is Sized → empty rule applies → error if empty string."""
    v = Validator({'x': {'type': 'string', 'empty': False}})
    assert v.validate({'x': ''}) is False


# ── _validate_dependencies ────────────────────────────────────────────────────
# p = isinstance(deps, str) OR NOT isinstance(deps, (Iterable, Mapping))
# DNF: A ∨ ¬B  (two implicants)
# UTP via A: deps is str → normalised to tuple → sequence path
# UTP via ¬B: deps is int (not Iterable/Mapping) → normalised to tuple → sequence path
# NFP (A=F, B=T): deps is list → predicate false → sequence path directly

def test_dep_string_dep_present():
    """deps is str (A=T) → dependency present → valid."""
    v = Validator({'x': {'dependencies': 'y'}, 'y': {}})
    assert v.validate({'x': 1, 'y': 2}) is True

def test_dep_string_dep_missing():
    """deps is str (A=T) → dependency missing → error."""
    v = Validator({'x': {'dependencies': 'y'}, 'y': {}})
    assert v.validate({'x': 1}) is False

def test_dep_list_dep_satisfied():
    """NFP: deps is list (A=F,B=T) → used directly → all deps present → valid."""
    v = Validator({'x': {'dependencies': ['y', 'z']}, 'y': {}, 'z': {}})
    assert v.validate({'x': 1, 'y': 1, 'z': 1}) is True

def test_dep_list_dep_missing_one():
    """NFP: deps is list → one dep missing → error."""
    v = Validator({'x': {'dependencies': ['y', 'z']}, 'y': {}, 'z': {}})
    assert v.validate({'x': 1, 'y': 1}) is False


# ── __validate_required_fields ────────────────────────────────────────────────
# p = document.get(field) is not None OR NOT ignore_none_values
# DNF: A ∨ ¬B
# UTP via A: ignore_none_values=True, field=non-None → field counts as present
# UTP via ¬B: ignore_none_values=False → all non-None and None fields count
# NFP (A=F, B=T): ignore_none_values=True, field=None → field not counted → missing error

def test_required_field_present():
    """Required field present with value → valid."""
    v = Validator({'x': {'required': True}})
    assert v.validate({'x': 1}) is True

def test_required_field_missing():
    """Required field absent → error."""
    v = Validator({'x': {'required': True}})
    assert v.validate({}) is False

def test_required_field_none_ignore_none_values():
    """NFP: ignore_none_values=True, field=None → field treated as absent → required error."""
    v = Validator({'x': {'required': True}}, ignore_none_values=True)
    assert v.validate({'x': None}) is False

def test_required_field_none_not_ignore():
    """¬B: ignore_none_values=False (default), required field present with None value.
    Cerberus still raises required error for None when nullable not set; use nullable=True."""
    v = Validator({'x': {'required': True, 'nullable': True}}, ignore_none_values=False)
    assert v.validate({'x': None}) is True


# ── _validate_regex ───────────────────────────────────────────────────────────
# p = isinstance(value, _str_type) AND NOT re_obj.match(value)
# UTP: value is string, doesn't match → error
# NFP-A: value is int → guard exits early, no regex check → no error
# NFP-B: value is string, matches pattern → no error

def test_regex_utp_string_no_match():
    """UTP: both clauses true → REGEX_MISMATCH error."""
    v = Validator({'x': {'type': 'string', 'regex': '^[0-9]+$'}})
    assert v.validate({'x': 'abc'}) is False

def test_regex_nfp_a_non_string():
    """NFP(A): value is int → not _str_type → guard returns early, no error."""
    v = Validator({'x': {'regex': '^[0-9]+$'}})
    assert v.validate({'x': 123}) is True

def test_regex_nfp_b_string_matches():
    """NFP(B): value matches regex → valid."""
    v = Validator({'x': {'type': 'string', 'regex': '^[0-9]+$'}})
    assert v.validate({'x': '123'}) is True

def test_regex_pattern_anchored():
    """Cerberus appends '$' to pattern → 'hello world' does not match '^hello$' → error.
    This tests the pattern mutation (pattern += '$') branch in _validate_regex."""
    v = Validator({'x': {'type': 'string', 'regex': '^hello'}})
    # '^hello' becomes '^hello$' → 'hello world' fails → error
    assert v.validate({'x': 'hello world'}) is False


# ── _validate_valuesrules ─────────────────────────────────────────────────────
# p_outer = isinstance(value, Mapping)
# p_inner = validator._errors (child validation fails)

def test_valuesrules_mapping_values_valid():
    """value is Mapping, all values pass valuesrules → valid."""
    v = Validator({'x': {'type': 'dict', 'valuesrules': {'type': 'integer'}}})
    assert v.validate({'x': {'a': 1, 'b': 2}}) is True

def test_valuesrules_mapping_value_invalid():
    """value is Mapping, one value fails valuesrules → error."""
    v = Validator({'x': {'type': 'dict', 'valuesrules': {'type': 'integer'}}})
    assert v.validate({'x': {'a': 1, 'b': 'not_int'}}) is False

def test_valuesrules_nfp_not_mapping():
    """NFP(outer): value is list → not Mapping → valuesrules skipped."""
    v = Validator({'x': {'valuesrules': {'type': 'integer'}}})
    assert v.validate({'x': [1, 2, 3]}) is True

def test_valuesrules_nested_type_check():
    """Values must be dicts with own type rules → invalid nested value → error."""
    v = Validator({'x': {'type': 'dict', 'valuesrules': {'type': 'string', 'minlength': 3}}})
    assert v.validate({'x': {'a': 'hi'}}) is False


# ── Additional fault-class analyses ──────────────────────────────────────────

# LDF · _validate_empty · F3-6
# Mutation: remove len(value)==0 → just isinstance(value, Sized)
# Revealing test: non-empty list with empty=False → valid; with LDF → every Sized errors.

def test_empty_ldf_b_deleted():
    """LDF(B): non-empty list with empty=False is valid; mutation drops len-check → error."""
    v = Validator({'x': {'type': 'list', 'empty': False}})
    assert v.validate({'x': [1, 2]}) is True


# LRF · _validate_empty · F3-7
# Mutation: len(value)==0 → len(value)==1
# Revealing test: single-element list with empty=False → valid; with LRF (len==1 True) → error.

def test_empty_lrf_single_element():
    """LRF: single-element list is not empty → valid; mutation (==1) fires for len-1 → error."""
    v = Validator({'x': {'type': 'list', 'empty': False}})
    assert v.validate({'x': [42]}) is True


# TNF · _validate_empty · F3-8
# Mutation: A∧B → ¬A∨¬B (not Sized OR len!=0)
# Revealing test: non-empty list, empty=False → valid; with TNF (¬A∨¬B: F∨T) → error.

def test_empty_tnf_non_empty():
    """TNF: non-empty list is valid; mutation (¬A∨¬B) fires when len!=0 → error."""
    v = Validator({'x': {'type': 'list', 'empty': False}})
    assert v.validate({'x': [1]}) is True


# TIF · _validate_regex · F3-9
# Mutation: add 'or not isinstance(value, str)' → non-strings also trigger regex error.
# Revealing test: integer value → guard returns early (valid); with TIF → error.

def test_regex_tif_non_string():
    """TIF: integer bypasses regex (guard exits); mutation adds ¬A term → integer errors."""
    v = Validator({'x': {'regex': '^[0-9]+$'}})
    assert v.validate({'x': 123}) is True


# ORF+ · _validate_dependencies · F3-10
# Mutation: A∨¬B → A∧¬B (isinstance(str) AND not isinstance(Iterable/Mapping))
# Since str IS Iterable, A∧¬B is always False → string deps not normalised → character iteration.
# Revealing test: deps='ab', field='ab' → normalised to ('ab',) → valid;
# with ORF+ → iterates 'a','b' → missing fields → error.

def test_dep_orf_plus_multichar_dep():
    """ORF+: string dep 'ab' normalised to ('ab',) → valid; mutation skips normalisation
    → iterates characters 'a','b' as separate dep field names → both missing → error."""
    v = Validator({'x': {'dependencies': 'ab'}, 'ab': {}})
    assert v.validate({'x': 1, 'ab': 1}) is True


# ORF* · _validate_regex · F3-11
# Mutation: A∧¬B → A∨¬B → string that matches still errors (A=True → OR=True).
# Revealing test: string matching pattern → valid; with ORF* → error.

def test_regex_orf_star_string_matches():
    """ORF*: matching string is valid; mutation (A∨¬B) fires when isinstance(str) is True → error."""
    v = Validator({'x': {'type': 'string', 'regex': '^[0-9]+$'}})
    assert v.validate({'x': '123'}) is True
