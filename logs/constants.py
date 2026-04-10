type_mapping = {
    "int": int,
    "float": (int, float),  # Allows int to be passed for float fields
    "string": str,
    "boolean": bool,
    "json": (dict, list),
}
