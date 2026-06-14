if isinstance(dependencies, _str_type) or not isinstance(
    dependencies, (Iterable, Mapping)
):
    dependencies = (dependencies,)