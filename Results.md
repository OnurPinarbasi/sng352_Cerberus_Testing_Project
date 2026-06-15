# Unit Tests
Here is the unit test cases and the results bellow:

|**File**|**Test Name**|**Status**|
|---|---|---|
|test_member1.py|test_type_utp_both_clauses_true_no_error|PASSED|
|test_member1.py|test_type_nfp_clause_a_false_error|PASSED|
|test_member1.py|test_type_nfp_clause_b_true_error|PASSED|
|test_member1.py|test_type_multiple_types_first_match|PASSED|
|test_member1.py|test_allowed_utp_list_all_allowed|PASSED|
|test_member1.py|test_allowed_nfp_a_non_iterable_scalar_unallowed|PASSED|
|test_member1.py|test_allowed_nfp_b_string_treated_as_scalar|PASSED|
|test_member1.py|test_allowed_utp_list_has_unallowed_element|PASSED|
|test_member1.py|test_unknown_fields_not_allowed_error|PASSED|
|test_member1.py|test_unknown_fields_allow_unknown_true|PASSED|
|test_member1.py|test_unknown_fields_allow_unknown_schema_valid|PASSED|
|test_member1.py|test_unknown_fields_allow_unknown_schema_invalid|PASSED|
|test_member1.py|test_minlength_utp_list_too_short|PASSED|
|test_member1.py|test_minlength_nfp_a_non_iterable|PASSED|
|test_member1.py|test_minlength_nfp_b_list_long_enough|PASSED|
|test_member1.py|test_minlength_string_too_short|PASSED|
|test_member1.py|test_dep_mapping_scalar_dep_value_satisfied|PASSED|
|test_member1.py|test_dep_mapping_scalar_dep_value_not_satisfied|PASSED|
|test_member1.py|test_dep_mapping_string_dep_value_satisfied|PASSED|
|test_member1.py|test_dep_mapping_list_dep_value_nfp|PASSED|
|test_member1.py|test_minlength_ldf_b_deleted|PASSED|
|test_member1.py|test_minlength_lrf_boundary|PASSED|
|test_member1.py|test_minlength_tnf_long_list|PASSED|
|test_member1.py|test_allowed_tif_integer_in_allowed|PASSED|
|test_member1.py|test_dep_mapping_orf_plus_int_dep|PASSED|
|test_member1.py|test_minlength_orf_star_long_list|PASSED|
|test_member1.py|test_allowed_enf_list_all_allowed|PASSED|
|test_member2.py|test_coerce_nonnullable_none_errors|PASSED|
|test_member2.py|test_coerce_nullable_non_none_coerces|PASSED|
|test_member2.py|test_coerce_nullable_none_suppressed|PASSED|
|test_member2.py|test_coerce_nonnullable_valid_value|PASSED|
|test_member2.py|test_excludes_conflict_error|PASSED|
|test_member2.py|test_excludes_no_conflict_valid|PASSED|
|test_member2.py|test_excludes_required_one_present|PASSED|
|test_member2.py|test_excludes_neither_present_required_fails|PASSED|
|test_member2.py|test_readonly_unnormalized_errors|PASSED|
|test_member2.py|test_readonly_normalized_no_value_change|PASSED|
|test_member2.py|test_readonly_normalized_value_present_errors|PASSED|
|test_member2.py|test_readonly_false_no_effect|PASSED|
|test_member2.py|test_maxlength_utp_list_too_long|PASSED|
|test_member2.py|test_maxlength_nfp_a_non_iterable|PASSED|
|test_member2.py|test_maxlength_nfp_b_within_limit|PASSED|
|test_member2.py|test_maxlength_string_too_long|PASSED|
|test_member2.py|test_keysrules_utp_mapping_keys_valid|PASSED|
|test_member2.py|test_keysrules_utp_mapping_keys_invalid|PASSED|
|test_member2.py|test_keysrules_nfp_outer_not_mapping|PASSED|
|test_member2.py|test_keysrules_mapping_regex_key_pattern|PASSED|
|test_member2.py|test_maxlength_ldf_b_deleted|PASSED|
|test_member2.py|test_maxlength_tnf_within_limit|PASSED|
|test_member2.py|test_maxlength_tif_non_iterable|PASSED|
|test_member2.py|test_coerce_orf_plus_nullable_bad_coerce|PASSED|
|test_member2.py|test_excludes_orf_star_required_missing|PASSED|
|test_member2.py|test_maxlength_enf_within_limit|PASSED|
|test_member3.py|test_empty_utp_empty_list_not_allowed|PASSED|
|test_member3.py|test_empty_utp_empty_list_allowed|PASSED|
|test_member3.py|test_empty_nfp_b_non_empty_list|PASSED|
|test_member3.py|test_empty_string_empty_not_allowed|PASSED|
|test_member3.py|test_dep_string_dep_present|PASSED|
|test_member3.py|test_dep_string_dep_missing|PASSED|
|test_member3.py|test_dep_list_dep_satisfied|PASSED|
|test_member3.py|test_dep_list_dep_missing_one|PASSED|
|test_member3.py|test_required_field_present|PASSED|
|test_member3.py|test_required_field_missing|PASSED|
|test_member3.py|test_required_field_none_ignore_none_values|PASSED|
|test_member3.py|test_required_field_none_not_ignore|PASSED|
|test_member3.py|test_regex_utp_string_no_match|PASSED|
|test_member3.py|test_regex_nfp_a_non_string|PASSED|
|test_member3.py|test_regex_nfp_b_string_matches|PASSED|
|test_member3.py|test_regex_pattern_anchored|PASSED|
|test_member3.py|test_valuesrules_mapping_values_valid|PASSED|
|test_member3.py|test_valuesrules_mapping_value_invalid|PASSED|
|test_member3.py|test_valuesrules_nfp_not_mapping|PASSED|
|test_member3.py|test_valuesrules_nested_type_check|PASSED|
|test_member3.py|test_empty_ldf_b_deleted|PASSED|
|test_member3.py|test_empty_lrf_single_element|PASSED|
|test_member3.py|test_empty_tnf_non_empty|PASSED|
|test_member3.py|test_regex_tif_non_string|PASSED|
|test_member3.py|test_dep_orf_plus_multichar_dep|PASSED|
|test_member3.py|test_regex_orf_star_string_matches|PASSED|
|test_member4.py|test_forbidden_utp_list_with_forbidden_element|PASSED|
|test_member4.py|test_forbidden_utp_list_no_forbidden|PASSED|
|test_member4.py|test_forbidden_nfp_a_scalar_forbidden|PASSED|
|test_member4.py|test_forbidden_nfp_b_string_scalar_check|PASSED|
|test_member4.py|test_schema_mapping_value_valid|PASSED|
|test_member4.py|test_schema_mapping_value_invalid|PASSED|
|test_member4.py|test_schema_sequence_value_valid|PASSED|
|test_member4.py|test_schema_sequence_value_invalid|PASSED|
|test_member4.py|test_contains_single_value_present|PASSED|
|test_member4.py|test_contains_single_value_absent|PASSED|
|test_member4.py|test_contains_list_expected_all_present|PASSED|
|test_member4.py|test_contains_list_expected_one_missing|PASSED|
|test_member4.py|test_normalize_coerce_field_in_schema|PASSED|
|test_member4.py|test_normalize_coerce_no_coerce_rule|PASSED|
|test_member4.py|test_normalize_coerce_unknown_field_with_allow_unknown_coerce|PASSED|
|test_member4.py|test_normalize_coerce_coerce_failure|PASSED|
|test_member4.py|test_items_length_mismatch|PASSED|
|test_member4.py|test_items_length_match_all_valid|PASSED|
|test_member4.py|test_items_length_match_one_invalid|PASSED|
|test_member4.py|test_items_three_items_all_valid|PASSED|
|test_member4.py|test_normalize_coerce_ldf_no_coerce_key|PASSED|
|test_member4.py|test_normalize_coerce_tnf_with_coerce|PASSED|
|test_member4.py|test_forbidden_tif_integer_not_forbidden|PASSED|
|test_member4.py|test_contains_orf_plus_string_multi|PASSED|
|test_member4.py|test_forbidden_orf_star_integer|PASSED|
|test_member4.py|test_forbidden_enf_list_with_forbidden|PASSED|


# Mutation test cases

Running all 45 mutant cases:

| **Test Subject**     | **type** | **function**                  | **result** |
| -------------------- | -------- | ----------------------------- | ---------- |
| Running mutant F1-1  | LIF      | _validate_type                | KILLED     |
| Running mutant F1-2  | LIF      | _validate_type                | SURVIVED   |
| Running mutant F1-3  | TOF      | _validate_allowed             | SURVIVED   |
| Running mutant F1-4  | LIF      | _validate_minlength           | KILLED     |
| Running mutant F1-5  | LNF      | validate_dependencies_mapping | SURVIVED   |
| Running mutant F2-1  | LNF      | normalize_coerce              | KILLED     |
| Running mutant F2-2  | LIF      | normalize_coerce              | SURVIVED   |
| Running mutant F2-3  | TOF      | _validate_excludes            | SURVIVED   |
| Running mutant F2-4  | LIF      | _validate_readonly            | SURVIVED   |
| Running mutant F2-5  | LRF      | _validate_maxlength           | SURVIVED   |
| Running mutant F3-1  | LIF      | _validate_empty               | SURVIVED   |
| Running mutant F3-2  | LNF      | _validate_dependencies        | KILLED     |
| Running mutant F3-3  | LIF      | validate_required_fields      | KILLED     |
| Running mutant F3-4  | TOF      | _validate_regex               | KILLED     |
| Running mutant F3-5  | ENF      | _validate_regex               | KILLED     |
| Running mutant F4-1  | TOF      | _validate_forbidden           | SURVIVED   |
| Running mutant F4-2  | LNF      | _validate_schema              | KILLED     |
| Running mutant F4-3  | LNF      | _validate_contains            | SURVIVED   |
| Running mutant F4-4  | LIF      | _normalize_coerce             | KILLED     |
| Running mutant F4-5  | LRF      | _validate_items               | KILLED     |
| Running mutant F1-6  | LDF      | _validate_minlength           | KILLED     |
| Running mutant F1-7  | LRF      | _validate_minlength           | KILLED     |
| Running mutant F1-8  | TNF      | _validate_minlength           | KILLED     |
| Running mutant F1-9  | TIF      | _validate_allowed             | KILLED     |
| Running mutant F1-10 | ORF+     | validate_dependencies_mapping | KILLED     |
| Running mutant F1-11 | ORF*     | _validate_minlength           | KILLED     |
| Running mutant F1-12 | ENF      | _validate_allowed             | KILLED     |
| Running mutant F2-6  | LDF      | _validate_maxlength           | KILLED     |
| Running mutant F2-7  | TNF      | _validate_maxlength           | KILLED     |
| Running mutant F2-8  | TIF      | _validate_maxlength           | KILLED     |
| Running mutant F2-9  | ORF+     | normalize_coerce              | KILLED     |
| Running mutant F2-10 | ORF      | _validate_excludes            | SURVIVED   |
| Running mutant F2-11 | ENF      | _validate_maxlength           | KILLED     |
| Running mutant F3-6  | LDF      | _validate_empty               | KILLED     |
| Running mutant F3-7  | LRF      | _validate_empty               | KILLED     |
| Running mutant F3-8  | TNF      | _validate_empty               | KILLED     |
| Running mutant F3-9  | TIF      | _validate_regex               | SURVIVED   |
| Running mutant F3-10 | ORF+     | _validate_dependencies        | KILLED     |
| Running mutant F3-11 | ORF      | _validate_regex               | KILLED     |
| Running mutant F4-6  | LDF      | _normalize_coerce             | KILLED     |
| Running mutant F4-7  | TNF      | _normalize_coerce             | KILLED     |
| Running mutant F4-8  | TIF      | _validate_forbidden           | KILLED     |
| Running mutant F4-9  | ORF+     | _validate_contains            | KILLED     |
| Running mutant F4-10 | ORF*     | _validate_forbidden           | KILLED     |
| Running mutant F4-11 | ENF      | _validate_forbidden           | KILLED     |

## Results

In this project, total 45 mutants tested and it can be seen that 33 of them killed.The percentage of detected tests are 73.3, this score can be seen as a successful result. In other words, this shows us that it will detect and identify errors in the vast majority of tests. The killing of mutants in different fault types shows that the test suite checks not only the basic states also it checks the logical behavior of the code. However, the survival of 12 mutants tells that tests can be improved for covering more of the edge cases. To conclude, the test framework worked practically ,and it was able to determine a significant percentage of errors.

| Metric                | Value      |
| --------------------- | ---------- |
| Total Mutants Checked | 45         |
| Killed (Detected)     | 33 (73.3%) |
| Survived (Undetected) | 12         |
| Errors/Skipped        | 0          |
