lst = [
    "DoesNotExist",
    "MultipleObjectsReturned",
    "Sex",
    "__class__",
    "__delattr__",
    "__dict__",
    "__dir__",
    "__doc__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__getstate__",
    "__gt__",
    "__hash__",
    "__init__",
    "__init_subclass__",
    "__le__",
    "__lt__",
    "__module__",
    "__ne__",
    "__new__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__setattr__",
    "__setstate__",
    "__sizeof__",
    "__str__",
    "__subclasshook__",
    "__weakref__",
    "_check_column_name_clashes",
    "_check_constraints",
    "_check_db_table_comment",
    "_check_default_pk",
    "_check_field_name_clashes",
    "_check_fields",
    "_check_id_field",
    "_check_index_together",
    "_check_indexes",
    "_check_local_fields",
    "_check_long_column_names",
    "_check_m2m_through_same_relationship",
    "_check_managers",
    "_check_model",
    "_check_model_name_db_lookup_clashes",
    "_check_ordering",
    "_check_property_name_related_field_accessor_clashes",
    "_check_single_primary_key",
    "_check_swappable",
    "_check_unique_together",
    "_do_insert",
    "_do_update",
    "_get_FIELD_display",
    "_get_expr_references",
    "_get_field_value_map",
    "_get_next_or_previous_by_FIELD",
    "_get_next_or_previous_in_order",
    "_get_pk_val",
    "_get_unique_checks",
    "_meta",
    "_perform_date_checks",
    "_perform_unique_checks",
    "_prepare_related_fields_for_save",
    "_save_parents",
    "_save_table",
    "_set_pk_val",
    "_state",
    "_validate_force_insert",
    "acceptedoffer_set",
    "adelete",
    "arefresh_from_db",
    "asave",
    "birth_country",
    "birth_date",
    "birth_town",
    "check",
    "clean",
    "clean_fields",
    "date_error_message",
    "delete",
    "education",
    "email",
    "familymember_set",
    "first_name",
    "foreign_language",
    "from_db",
    "full_clean",
    "full_name",
    "get_constraints",
    "get_deferred_fields",
    "get_next_by_birth_date",
    "get_previous_by_birth_date",
    "get_sex_display",
    "id",
    "last_name",
    "living_address",
    "nationality",
    "objects",
    "patronymic",
    "phone_set",
    "pk",
    "prepare_database_save",
    "refresh_from_db",
    "registered_address",
    "save",
    "save_base",
    "serializable_value",
    "sex",
    "unique_error_message",
    "validate_constraints",
    "validate_unique",
    "work",
]

print([x for x in lst if x.endswith("set")])