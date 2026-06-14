"""
Member 4 – Functions: _validate_forbidden, _validate_schema,
_validate_contains, _normalize_coerce, _validate_items

MUMCUT predicates:
  _validate_forbidden : p = isinstance(value, Sequence) ∧ ¬isinstance(value, str)
  _validate_schema    : p = isinstance(value, Sequence) ∧ ¬isinstance(value, str)
                        (elif branch: isinstance(value, Mapping))
  _validate_contains  : p = ¬isinstance(exp, Iterable) ∨ isinstance(exp, str)
  _normalize_coerce   : p = (field in schema) ∧ ('coerce' in schema[field])
  _validate_items     : p1 = len(items)≠len(values); p2 = ¬validator(ok)
"""
import pytest
from cerberus import Validator


# ── _validate_forbidden ───────────────────────────────────────────────────────
# p = isinstance(value, Sequence) AND NOT isinstance(value, _str_type)
# UTP: list value → membership check per element
# NFP-A: integer → scalar check
# NFP-B: string → scalar check

def test_forbidden_utp_list_with_forbidden_element():
    """UTP: list contains forbidden value → error."""
    v = Validator({'x': {'type': 'list', 'forbidden': [2, 3]}})
    assert v.validate({'x': [1, 2]}) is False

def test_forbidden_utp_list_no_forbidden():
    """UTP: list with no forbidden values → valid."""
    v = Validator({'x': {'type': 'list', 'forbidden': [9, 10]}})
    assert v.validate({'x': [1, 2]}) is True

def test_forbidden_nfp_a_scalar_forbidden():
    """NFP(A): integer is in forbidden list → scalar path → error."""
    v = Validator({'x': {'forbidden': [1, 2, 3]}})
    assert v.validate({'x': 2}) is False

def test_forbidden_nfp_b_string_scalar_check():
    """NFP(B): string value → scalar check (not element-wise) → not in list → valid."""
    v = Validator({'x': {'forbidden': ['hello']}})
    assert v.validate({'x': 'world'}) is True


# ── _validate_schema ──────────────────────────────────────────────────────────
# p1 = isinstance(value, Sequence) AND NOT isinstance(value, str) → sequence path
# p2 (elif) = isinstance(value, Mapping) → mapping path

def test_schema_mapping_value_valid():
    """value is dict → mapping path → sub-schema validates → valid."""
    v = Validator({'x': {'type': 'dict', 'schema': {'a': {'type': 'integer'}}}})
    assert v.validate({'x': {'a': 1}}) is True

def test_schema_mapping_value_invalid():
    """value is dict → mapping path → sub-schema fails → error."""
    v = Validator({'x': {'type': 'dict', 'schema': {'a': {'type': 'integer'}}}})
    assert v.validate({'x': {'a': 'not_int'}}) is False

def test_schema_sequence_value_valid():
    """value is list (Sequence, not str) → sequence path → each item validated → valid."""
    v = Validator({'x': {'type': 'list', 'schema': {'type': 'integer'}}})
    assert v.validate({'x': [1, 2, 3]}) is True

def test_schema_sequence_value_invalid():
    """value is list → sequence path → item fails schema → error."""
    v = Validator({'x': {'type': 'list', 'schema': {'type': 'integer'}}})
    assert v.validate({'x': [1, 'bad', 3]}) is False


# ── _validate_contains ────────────────────────────────────────────────────────
# p = NOT isinstance(expected_values, Iterable) OR isinstance(expected_values, str)
# DNF: ¬A ∨ B
# UTP via B: expected_values is str → normalised to set of one value
# NFP (A=T, B=F): expected_values is list → predicate false → used directly as set

def test_contains_single_value_present():
    """expected_values is scalar str → normalised; value contains it → valid."""
    v = Validator({'x': {'type': 'list', 'contains': 'a'}})
    assert v.validate({'x': ['a', 'b']}) is True

def test_contains_single_value_absent():
    """expected_values is str → normalised; value doesn't contain it → error."""
    v = Validator({'x': {'type': 'list', 'contains': 'z'}})
    assert v.validate({'x': ['a', 'b']}) is False

def test_contains_list_expected_all_present():
    """NFP: expected_values is list (A=T,B=F) → used directly → all found → valid."""
    v = Validator({'x': {'type': 'list', 'contains': ['a', 'b']}})
    assert v.validate({'x': ['a', 'b', 'c']}) is True

def test_contains_list_expected_one_missing():
    """NFP: expected_values is list → one missing → error."""
    v = Validator({'x': {'type': 'list', 'contains': ['a', 'z']}})
    assert v.validate({'x': ['a', 'b']}) is False


# ── _normalize_coerce (public) ────────────────────────────────────────────────
# p_if  = (field in schema) AND ('coerce' in schema[field])
# p_elif = isinstance(self.allow_unknown, Mapping) AND ('coerce' in self.allow_unknown)
# UTP(p_if): field in schema with coerce rule → coerce applied
# NFP-if-A: field not in schema → elif checked
# NFP-if-B: field in schema but no 'coerce' → no coerce applied

def test_normalize_coerce_field_in_schema():
    """p_if both true: field has coerce → value converted → valid."""
    v = Validator({'x': {'coerce': int, 'type': 'integer'}})
    assert v.validate({'x': '42'}) is True

def test_normalize_coerce_no_coerce_rule():
    """NFP(B): field in schema, no coerce → no conversion → type error on string."""
    v = Validator({'x': {'type': 'integer'}})
    assert v.validate({'x': '42'}) is False

def test_normalize_coerce_unknown_field_with_allow_unknown_coerce():
    """p_elif: unknown field with allow_unknown containing coerce → coerced."""
    v = Validator({}, allow_unknown={'coerce': int, 'type': 'integer'})
    result = v.validated({'z': '99'})
    assert result == {'z': 99}

def test_normalize_coerce_coerce_failure():
    """Coerce raises exception → error filed."""
    v = Validator({'x': {'coerce': int, 'type': 'integer'}})
    assert v.validate({'x': 'not_a_number'}) is False


# ── _validate_items ───────────────────────────────────────────────────────────
# p1 = len(items) != len(values) → error immediately
# p2 (else) = NOT validator(dict of values) → child validation error

def test_items_length_mismatch():
    """p1 true: items count != values count → ITEMS_LENGTH error."""
    v = Validator({'x': {'type': 'list', 'items': [{'type': 'integer'}, {'type': 'string'}]}})
    assert v.validate({'x': [1]}) is False

def test_items_length_match_all_valid():
    """p1 false, p2 false: lengths match, all items valid → valid."""
    v = Validator({'x': {'type': 'list', 'items': [{'type': 'integer'}, {'type': 'string'}]}})
    assert v.validate({'x': [1, 'hello']}) is True

def test_items_length_match_one_invalid():
    """p1 false, p2 true: lengths match, second item wrong type → error."""
    v = Validator({'x': {'type': 'list', 'items': [{'type': 'integer'}, {'type': 'string'}]}})
    assert v.validate({'x': [1, 2]}) is False

def test_items_three_items_all_valid():
    """Longer items list, all correct types → valid."""
    v = Validator({'x': {'type': 'list', 'items': [
        {'type': 'integer'}, {'type': 'string'}, {'type': 'boolean'}
    ]}})
    assert v.validate({'x': [1, 'ok', True]}) is True


# ── Additional fault-class analyses ──────────────────────────────────────────

# LDF · _normalize_coerce · F4-6
# Mutation: remove 'coerce' in schema[field] → just field in schema
# Revealing test: field in schema, no coerce rule, valid integer → should pass;
# with LDF → tries to call missing coerce key → error.

def test_normalize_coerce_ldf_no_coerce_key():
    """LDF(B): integer field with no coerce rule is valid; mutation drops coerce-key check
    → coerce attempted on every schema field → error."""
    v = Validator({'x': {'type': 'integer'}})
    assert v.validate({'x': 5}) is True


# TNF · _normalize_coerce · F4-7
# Mutation: A∧B → ¬A∨¬B (field not in schema OR no coerce key)
# Revealing test: field with coerce=int, value='5' → coerced → valid;
# with TNF (¬A∨¬B: F∨F=F) → coerce skipped → '5' fails type check → error.

def test_normalize_coerce_tnf_with_coerce():
    """TNF: coerce=int converts '5' → integer → valid; mutation negates condition
    → coerce not applied → string fails type check → error."""
    v = Validator({'x': {'coerce': int, 'type': 'integer'}})
    assert v.validate({'x': '5'}) is True


# TIF · _validate_forbidden · F4-8
# Mutation: add 'or isinstance(value, int)' → integers enter list-iteration path → TypeError.
# Revealing test: integer not in forbidden list → valid via scalar; with TIF → error.

def test_forbidden_tif_integer_not_forbidden():
    """TIF: integer not in forbidden list is valid; mutation adds int term → list path
    → TypeError → error."""
    v = Validator({'x': {'forbidden': [9, 10]}})
    assert v.validate({'x': 5}) is True


# ORF+ · _validate_contains · F4-9
# Mutation: ¬A∨B → ¬A∧B (always False since str IS Iterable)
# → string expected_values not normalised → iterated as characters.
# Revealing test: contains='abc', value=['abc'] → normalised → valid;
# with ORF+ → checks 'a','b','c' in ['abc'] → missing → error.

def test_contains_orf_plus_string_multi():
    """ORF+: contains='abc' normalised to ('abc',) → 'abc' in list → valid;
    mutation skips normalisation → checks chars 'a','b','c' → not found → error."""
    v = Validator({'x': {'type': 'list', 'contains': 'abc'}})
    assert v.validate({'x': ['abc']}) is True


# ORF* · _validate_forbidden · F4-10
# Mutation: A∧¬B → A∨¬B → integers (A=F, B=F → ¬B=T) enter list path → TypeError.
# Revealing test: integer not in forbidden → valid via scalar; with ORF* → error.

def test_forbidden_orf_star_integer():
    """ORF*: integer not in forbidden is valid; mutation (A∨¬B) sends int to list path
    → TypeError → error."""
    v = Validator({'x': {'forbidden': [9, 10]}})
    assert v.validate({'x': 7}) is True


# ENF · _validate_forbidden · F4-11
# Mutation: negate whole predicate → lists bypass element check → scalar check.
# Revealing test: list containing a forbidden element → should error;
# with ENF → list as scalar not in forbidden list → valid.

def test_forbidden_enf_list_with_forbidden():
    """ENF: list [1,2] contains forbidden 2 → should error; mutation negates predicate
    → list treated as scalar → not in [2,3] → incorrectly valid."""
    v = Validator({'x': {'type': 'list', 'forbidden': [2, 3]}})
    assert v.validate({'x': [1, 2]}) is False
