from functools import reduce


def get_nested(storage: dict, *keys):
    """
    Get a value from a nested dictionary.

    Args:
        storage (dict): The dictionary to retrieve the value from.
        *keys (str): The keys of the nested dictionary, in order.

    Returns:
        Any | None: The value of the specified key in the nested dictionary, or None if the key does not exist.
    """
    return reduce(
        lambda value, key: value.get(key, None) if isinstance(value, dict) else None,
        keys,
        storage,
    )
