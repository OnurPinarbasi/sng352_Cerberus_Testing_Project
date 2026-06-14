if isinstance(dependencies, _str_type) and not isinstance(
    dependencies, (Iterable, Mapping)
):
    dependencies = (dependencies,)