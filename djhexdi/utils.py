def sanitinze_hexdi_module_name(name: str):
    if name.endswith('.py'):
        return name
    return "{}.py".format(name)
