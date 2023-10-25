def check_structure(struct, schema):
    if isinstance(struct, dict) and isinstance(schema, dict):
        # struct is a dict of types or other dicts
        return all(
            k in schema and check_structure(struct[k], schema[k]) for k in struct
        )
    if isinstance(struct, list) and isinstance(schema, list):
        # struct is list in the form [type or dict]
        return all(check_structure(struct[0], c) for c in schema)
    elif isinstance(schema, type):
        # struct is the type of schema
        return isinstance(struct, schema)
    else:
        # struct is neither a dict, nor list, not type
        return False
