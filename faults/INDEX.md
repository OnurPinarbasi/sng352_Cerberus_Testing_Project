# Implemented Mutations Index

This index lists all 45 fault-emulating mutations implemented in this project. Each mutation is placed in its own folder and can be applied to the SUT via its patch file.

| Mutation ID | Fault Class | Target File | Target Function | Killing Test | Artifact Folder |
|-------------|-------------|-------------|-----------------|--------------|-----------------|
| F1-1 | LIF | cerberus/validator.py | _validate_type | tests/member1/test_member1.py::test_type_nfp_clause_a_false_error | faults/F1-1 |
| F1-2 | LIF | cerberus/validator.py | _validate_type | tests/member1/test_member1.py::test_type_nfp_clause_b_true_error | faults/F1-2 |
| F1-3 | TOF | cerberus/validator.py | _validate_allowed | tests/member1/test_member1.py::test_allowed_nfp_b_string_treated_as_scalar | faults/F1-3 |
| F1-4 | LIF | cerberus/validator.py | _validate_minlength | tests/member1/test_member1.py::test_minlength_nfp_a_non_iterable | faults/F1-4 |
| F1-5 | LNF | cerberus/validator.py | __validate_dependencies_mapping | tests/member1/test_member1.py::test_dep_mapping_list_dep_value_nfp | faults/F1-5 |
| F2-1 | LNF | cerberus/validator.py | __normalize_coerce | tests/member2/test_member2.py::test_coerce_nullable_none_suppressed | faults/F2-1 |
| F2-2 | LIF | cerberus/validator.py | __normalize_coerce | tests/member2/test_member2.py::test_coerce_nonnullable_none_errors | faults/F2-2 |
| F2-3 | TOF | cerberus/validator.py | _validate_excludes | tests/member2/test_member2.py::test_excludes_neither_present_required_fails | faults/F2-3 |
| F2-4 | LIF | cerberus/validator.py | _validate_readonly | tests/member2/test_member2.py::test_readonly_unnormalized_errors | faults/F2-4 |
| F2-5 | LRF | cerberus/validator.py | _validate_maxlength | tests/member2/test_member2.py::test_maxlength_nfp_b_within_limit | faults/F2-5 |
| F3-1 | LIF | cerberus/validator.py | _validate_empty | TODO: Any test passing a non-Sized type when the empty rule is present. | faults/F3-1 |
| F3-2 | LNF | cerberus/validator.py | _validate_dependencies | tests/member3/test_member3.py::test_dep_list_dep_satisfied | faults/F3-2 |
| F3-3 | LIF | cerberus/validator.py | __validate_required_fields | tests/member3/test_member3.py::test_required_field_none_ignore_none_values | faults/F3-3 |
| F3-4 | TOF | cerberus/validator.py | _validate_regex | tests/member3/test_member3.py::test_regex_nfp_a_non_string | faults/F3-4 |
| F3-5 | ENF | cerberus/validator.py | _validate_regex | tests/member3/test_member3.py::test_regex_utp_string_no_match | faults/F3-5 |
| F4-1 | TOF | cerberus/validator.py | _validate_forbidden | tests/member4/test_member4.py::test_forbidden_nfp_b_string_scalar_check | faults/F4-1 |
| F4-2 | LNF | cerberus/validator.py | _validate_schema | tests/member4/test_member4.py::test_schema_sequence_value_invalid | faults/F4-2 |
| F4-3 | LNF | cerberus/validator.py | _validate_contains | tests/member4/test_member4.py::test_contains_list_expected_all_present | faults/F4-3 |
| F4-4 | LIF | cerberus/validator.py | _normalize_coerce | tests/member4/test_member4.py::test_normalize_coerce_no_coerce_rule | faults/F4-4 |
| F4-5 | LRF | cerberus/validator.py | _validate_items | tests/member4/test_member4.py::test_items_length_mismatch | faults/F4-5 |
| F1-6 | LDF | cerberus/validator.py | _validate_minlength | tests/member1/test_member1.py::test_minlength_ldf_b_deleted | faults/F1-6 |
| F1-7 | LRF | cerberus/validator.py | _validate_minlength | tests/member1/test_member1.py::test_minlength_lrf_boundary | faults/F1-7 |
| F1-8 | TNF | cerberus/validator.py | _validate_minlength | tests/member1/test_member1.py::test_minlength_tnf_long_list | faults/F1-8 |
| F1-9 | TIF | cerberus/validator.py | _validate_allowed | tests/member1/test_member1.py::test_allowed_tif_integer_in_allowed | faults/F1-9 |
| F1-10 | ORF+ | cerberus/validator.py | __validate_dependencies_mapping | tests/member1/test_member1.py::test_dep_mapping_orf_plus_int_dep | faults/F1-10 |
| F1-11 | ORF* | cerberus/validator.py | _validate_minlength | tests/member1/test_member1.py::test_minlength_orf_star_long_list | faults/F1-11 |
| F1-12 | ENF | cerberus/validator.py | _validate_allowed | tests/member1/test_member1.py::test_allowed_enf_list_all_allowed | faults/F1-12 |
| F2-6 | LDF | cerberus/validator.py | _validate_maxlength | tests/member2/test_member2.py::test_maxlength_ldf_b_deleted | faults/F2-6 |
| F2-7 | TNF | cerberus/validator.py | _validate_maxlength | tests/member2/test_member2.py::test_maxlength_tnf_within_limit | faults/F2-7 |
| F2-8 | TIF | cerberus/validator.py | _validate_maxlength | tests/member2/test_member2.py::test_maxlength_tif_non_iterable | faults/F2-8 |
| F2-9 | ORF+ | cerberus/validator.py | __normalize_coerce | tests/member2/test_member2.py::test_coerce_orf_plus_nullable_bad_coerce | faults/F2-9 |
| F2-10 | ORF* | cerberus/validator.py | _validate_excludes | tests/member2/test_member2.py::test_excludes_orf_star_required_missing | faults/F2-10 |
| F2-11 | ENF | cerberus/validator.py | _validate_maxlength | tests/member2/test_member2.py::test_maxlength_enf_within_limit | faults/F2-11 |
| F3-6 | LDF | cerberus/validator.py | _validate_empty | tests/member3/test_member3.py::test_empty_ldf_b_deleted | faults/F3-6 |
| F3-7 | LRF | cerberus/validator.py | _validate_empty | tests/member3/test_member3.py::test_empty_lrf_single_element | faults/F3-7 |
| F3-8 | TNF | cerberus/validator.py | _validate_empty | tests/member3/test_member3.py::test_empty_tnf_non_empty | faults/F3-8 |
| F3-9 | TIF | cerberus/validator.py | _validate_regex | tests/member3/test_member3.py::test_regex_tif_non_string | faults/F3-9 |
| F3-10 | ORF+ | cerberus/validator.py | _validate_dependencies | tests/member3/test_member3.py::test_dep_orf_plus_multichar_dep | faults/F3-10 |
| F3-11 | ORF* | cerberus/validator.py | _validate_regex | tests/member3/test_member3.py::test_regex_orf_star_string_matches | faults/F3-11 |
| F4-6 | LDF | cerberus/validator.py | _normalize_coerce | tests/member4/test_member4.py::test_normalize_coerce_ldf_no_coerce_key | faults/F4-6 |
| F4-7 | TNF | cerberus/validator.py | _normalize_coerce | tests/member4/test_member4.py::test_normalize_coerce_tnf_with_coerce | faults/F4-7 |
| F4-8 | TIF | cerberus/validator.py | _validate_forbidden | tests/member4/test_member4.py::test_forbidden_tif_integer_not_forbidden | faults/F4-8 |
| F4-9 | ORF+ | cerberus/validator.py | _validate_contains | tests/member4/test_member4.py::test_contains_orf_plus_string_multi | faults/F4-9 |
| F4-10 | ORF* | cerberus/validator.py | _validate_forbidden | tests/member4/test_member4.py::test_forbidden_orf_star_integer | faults/F4-10 |
| F4-11 | ENF | cerberus/validator.py | _validate_forbidden | tests/member4/test_member4.py::test_forbidden_enf_list_with_forbidden | faults/F4-11 |
