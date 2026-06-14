if isinstance(dependencies, _str_type) or isinstance(
    dependencies, (Iterable, Mapping)
):
    dependencies = (dependencies,)