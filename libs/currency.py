from json import load, dump
from math import exp, log
from os.path import exists

FILENAME = "./res/money.json"

_money = dict()
_tax = dict()
_totalv = 1000000000
_frozen = 1000000000
_owners = dict()
UNIT = "mE"

try:
    with open(FILENAME, "r") as file:
        data = load(file)
    _money = data["money"]
    _tax = data["tax"]
    _totalv = data["totalv"]
    _owners = data["owners"]
except:
    pass

_frozen = _totalv - sum(_money.values())


def get_money(user_id):
    return _money.get(str(user_id), 0)


def set_money(user_id, amount):
    _money[str(user_id)] = amount
    _dump()


def get_tax(user_id):
    return _tax.get(str(user_id), 0)


def set_tax(user_id, amount):
    _tax[str(user_id)] = amount
    _dump()


def set_owners(of: str, whos: list[int]):
    _owners[of] = whos
    _dump()


def get_owners(of: str):
    return _owners.get(of)


def is_account(named: str):
    return named in _money or named in _owners


def get_accounts_of(who):
    result = list()
    for acc, owners in _owners.items():
        if who not in owners:
            continue
        result.append(acc)
    return result


def rotate(value):
    global _frozen
    delta = round(_frozen * (exp(value / _totalv) - 1))
    _frozen -= delta
    return delta


def freeze(amount: int) -> int:
    global _frozen
    _frozen -= amount
    value = round(_totalv * log(amount / _frozen + 1))
    return value


def _dump():
    with open(FILENAME, "w") as file:
        dump({
            "money": _money,
            "totalv": _totalv,
            "frozen": _frozen,
            "owners": _owners,
            "tax": _tax,
        }, file)
