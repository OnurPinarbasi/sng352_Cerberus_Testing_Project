"""
Member 2 – Functions: __normalize_coerce, _validate_excludes,
_validate_readonly, _validate_maxlength, _validate_keysrules

MUMCUT predicates:
  __normalize_coerce   : p = ¬(nullable ∧ (value is None))  → DNF: ¬A ∨ ¬B
  _validate_excludes   : p = (excl_field in schema) ∧ schema[field].get('required', require_all)
  _validate_readonly   : p = self._is_normalized ∧ has_error
  _validate_maxlength  : p = isinstance(value, Iterable) ∧ len(value) > max_length
  _validate_keysrules  : p_outer = isinstance(value, Mapping); p_inner = ¬validator(ok)
"""
import pytest
from cerberus import Validator


# ── __normalize_coerce ────────────────────────────────────────────────────────
# p = NOT (nullable AND value is None)
# DNF: ¬nullable ∨ ¬(value is None)  i.e.  ¬A ∨ ¬B
# UTP via ¬A: nullable=False, value=None  → error filed (coerce fails, not suppressed)
# UTP via ¬B: nullable=True,  value=42   → coerce attempted normally
# NFP (A∧B true → p false): nullable=True, value=None → error suppressed → no error

def test_coerce_nonnullable_none_errors():
    """¬A=T (nullable=False), value=None → coerce exception not suppressed → error."""
    v = Validator({'x': {'coerce': int, 'nullable': False}})
    assert v.validate({'x': None}) is False

def test_coerce_nullable_non_none_coerces():
    """¬B=T (value≠None), nullable=True → coerce runs normally → valid."""
    v = Validator({'x': {'coerce': int, 'nullable': True}})
    assert v.validate({'x': '5'}) is True

def test_coerce_nullable_none_suppressed():
    """NFP: A∧B → p=False → exception suppressed → no coerce error."""
    v = Validator({'x': {'coerce': int, 'nullable': True}})
    assert v.validate({'x': None}) is True

def test_coerce_nonnullable_valid_value():
    """¬A=T, ¬B=T → coerce runs, value convertible → valid."""
    v = Validator({'x': {'coerce': int, 'nullable': False}})
    assert v.validate({'x': '7'}) is True


# ── _validate_excludes ────────────────────────────────────────────────────────
# p = (excl_field in self.schema) AND self.schema[field].get('required', require_all)
# UTP: both true → excluded field added to _unrequired_by_excludes
# NFP-A: excl_field not in schema → only current field marked, no unrequired for excluded
# NFP-B: field not required → skip marking excluded field unrequired

def test_excludes_conflict_error():
    """Both excluded fields present → excludes violation error."""
    v = Validator({'x': {'excludes': 'y'}, 'y': {}})
    assert v.validate({'x': 1, 'y': 2}) is False

def test_excludes_no_conflict_valid():
    """Only one of the mutually exclusive fields present → valid."""
    v = Validator({'x': {'excludes': 'y'}, 'y': {}})
    assert v.validate({'x': 1}) is True

def test_excludes_required_one_present():
    """required + excludes: one present → satisfies requirement."""
    v = Validator({'x': {'required': True, 'excludes': 'y'}, 'y': {'required': True, 'excludes': 'x'}})
    assert v.validate({'x': 1}) is True

def test_excludes_neither_present_required_fails():
    """required + excludes: neither present → required error."""
    v = Validator({'x': {'required': True, 'excludes': 'y'}, 'y': {'required': True, 'excludes': 'x'}})
    assert v.validate({}) is False


# ── _validate_readonly ────────────────────────────────────────────────────────
# p_outer = readonly (True)
# p_inner_1 = NOT self._is_normalized (line 1415) → error if document not normalized
# p_inner_2 = self._is_normalized AND has_error (line 1426) → drop rules if already errored
# UTP(p_inner_2): normalize=True (is_normalized=T), readonly field present → has_error=T → drop rules

def test_readonly_unnormalized_errors():
    """readonly=True, normalize=False → _is_normalized=False → READONLY_FIELD error."""
    v = Validator({'x': {'readonly': True}})
    assert v.validate({'x': 1}, normalize=False) is False

def test_readonly_normalized_no_value_change():
    """readonly=True, normalize=True, field not in document → no error (field absent)."""
    v = Validator({'x': {'readonly': True, 'default': 5}})
    assert v.validate({}) is True

def test_readonly_normalized_value_present_errors():
    """readonly=True, normalize=True, field in document → READONLY_FIELD error."""
    v = Validator({'x': {'readonly': True}})
    assert v.validate({'x': 10}, normalize=True) is False

def test_readonly_false_no_effect():
    """readonly=False → no readonly constraint → valid."""
    v = Validator({'x': {'readonly': False}})
    assert v.validate({'x': 10}) is True


# ── _validate_maxlength ───────────────────────────────────────────────────────
# p = isinstance(value, Iterable) AND len(value) > max_length
# UTP: list with len > max → error
# NFP-A: integer (not Iterable) → no check
# NFP-B: list with len <= max → valid

def test_maxlength_utp_list_too_long():
    """UTP: both clauses true → maxlength error."""
    v = Validator({'x': {'type': 'list', 'maxlength': 2}})
    assert v.validate({'x': [1, 2, 3]}) is False

def test_maxlength_nfp_a_non_iterable():
    """NFP(A): integer not Iterable → maxlength not enforced."""
    v = Validator({'x': {'maxlength': 2}})
    assert v.validate({'x': 99}) is True

def test_maxlength_nfp_b_within_limit():
    """NFP(B): list within limit → valid."""
    v = Validator({'x': {'type': 'list', 'maxlength': 5}})
    assert v.validate({'x': [1, 2]}) is True

def test_maxlength_string_too_long():
    """String is Iterable → maxlength applies → error when too long."""
    v = Validator({'x': {'type': 'string', 'maxlength': 3}})
    assert v.validate({'x': 'hello'}) is False


# ── _validate_keysrules ───────────────────────────────────────────────────────
# p_outer = isinstance(value, Mapping)
# p_inner = NOT validator(keys) (child validator fails)

def test_keysrules_utp_mapping_keys_valid():
    """value is Mapping, keys pass keysrules → valid."""
    v = Validator({'x': {'type': 'dict', 'keysrules': {'type': 'string'}}})
    assert v.validate({'x': {'a': 1, 'b': 2}}) is True

def test_keysrules_utp_mapping_keys_invalid():
    """value is Mapping, key fails keysrules type check → error."""
    v = Validator({'x': {'keysrules': {'type': 'string', 'minlength': 3}}})
    assert v.validate({'x': {'ab': 1}}) is False

def test_keysrules_nfp_outer_not_mapping():
    """NFP(outer): value is list → not Mapping → keysrules skipped → valid."""
    v = Validator({'x': {'keysrules': {'type': 'string'}}})
    assert v.validate({'x': [1, 2, 3]}) is True

def test_keysrules_mapping_regex_key_pattern():
    """Keys must match regex pattern via keysrules → invalid key → error."""
    v = Validator({'x': {'type': 'dict', 'keysrules': {'type': 'string', 'regex': '^[a-z]+$'}}})
    assert v.validate({'x': {'ABC': 1}}) is False


# ── Additional fault-class analyses ──────────────────────────────────────────

# LDF · _validate_maxlength · F2-6
# Mutation: remove len(value)>max_length → just isinstance(value, Iterable)
# Revealing test: list within limit → valid; with LDF → every Iterable errors.

def test_maxlength_ldf_b_deleted():
    """LDF(B): list within limit is valid; mutation drops len-check → error."""
    v = Validator({'x': {'type': 'list', 'maxlength': 5}})
    assert v.validate({'x': [1, 2]}) is True


# TNF · _validate_maxlength · F2-7
# Mutation: A∧B → ¬A∨¬B (not Iterable OR len<=max)
# Revealing test: list within limit → valid; with TNF (¬A∨¬B: F∨T) → error.

def test_maxlength_tnf_within_limit():
    """TNF: within-limit list is valid; mutation (¬A∨¬B) fires when len<=max → error."""
    v = Validator({'x': {'type': 'list', 'maxlength': 5}})
    assert v.validate({'x': [1, 2]}) is True


# TIF · _validate_maxlength · F2-8
# Mutation: add 'or not isinstance(value, Iterable)' → non-Iterables also error.
# Revealing test: integer (not Iterable) → no check → valid; with TIF → error.

def test_maxlength_tif_non_iterable():
    """TIF: integer bypasses maxlength check; mutation adds non-Iterable term → error."""
    v = Validator({'x': {'maxlength': 5}})
    assert v.validate({'x': 3}) is True


# ORF+ · __normalize_coerce · F2-9
# Mutation: ¬A∨¬B → ¬A∧¬B (not nullable AND value is not None)
# Revealing test: nullable=True, value='bad' (coerce fails) → exception propagated → error;
# with ORF+ (¬A∧¬B: F∧T=F) → exception suppressed → valid.

def test_coerce_orf_plus_nullable_bad_coerce():
    """ORF+: nullable=True, bad coerce value → exception should propagate → error;
    mutation (¬A∧¬B) suppresses it → incorrectly valid."""
    v = Validator({'x': {'coerce': int, 'nullable': True}})
    assert v.validate({'x': 'not_a_number'}) is False


# ORF* · _validate_excludes · F2-10
# Mutation: A∧B → A∨B → excluded field wrongly exempted from required check.
# Revealing test: y required, x (not required) excludes y, document={x:1} →
# y should still be required → error; with ORF* → y exempted → valid.

def test_excludes_orf_star_required_missing():
    """ORF*: required field y not exempted when non-required x excludes it;
    mutation (A∨B) wrongly exempts y → missing required field goes undetected."""
    v = Validator({
        'x': {'excludes': 'y'},
        'y': {'required': True}
    })
    assert v.validate({'x': 1}) is False


# ENF · _validate_maxlength · F2-11
# Mutation: negate whole predicate → within-limit values error; over-limit values pass.
# Revealing test: list within limit → valid; with ENF → error.

def test_maxlength_enf_within_limit():
    """ENF: within-limit list is valid; mutation negates predicate → fires for valid input."""
    v = Validator({'x': {'type': 'list', 'maxlength': 5}})
    assert v.validate({'x': [1, 2]}) is True
