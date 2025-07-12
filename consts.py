from typing import Optional, Any
from json import load

with open("res/consts.json", "r") as file:
    consts = load(file)

with open("res/secrets.json", "r") as file:
    secrets = load(file)


def _get(dictionary, path) -> Optional[Any]:
    paths = path.split(".")

    while paths:
        dictionary = dictionary.get(paths.pop(0))

        if dictionary is None:
            raise NameError(f'value with key {path} not found')

    return dictionary


def _set(dictionary, path, value):
    path = path.split(".")

    while len(path) > 1:
        dictionary = dictionary.get(path.pop(0))

    dictionary[path.pop()] = value


def get_const(path):
    return _get(consts, path)


def override_const(path, value):
    _set(consts, path, value)


def get_secret(path):
    return _get(secrets, path)
