from os.path import getsize


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


def format_file_size(file_size):
    if file_size < 1000:
        return f"{file_size} o"

    size_in_KB = file_size / (2**10)
    if size_in_KB < 1000:
        return ("%.1f Ko" % size_in_KB).replace(".", ",")

    size_in_MB = size_in_KB / (2**10)
    if size_in_MB < 1000:
        return ("%.1f Mo" % size_in_MB).replace(".", ",")

    size_in_GB = size_in_MB / (2**10)
    return ("%.1f Go" % size_in_GB).replace(".", ",")


def get_formatted_file_size(file_path):
    file_size = getsize(file_path)
    return format_file_size(file_size)
