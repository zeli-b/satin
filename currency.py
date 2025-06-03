from math import exp
from os.path import exists

FILENAME = "./res/money.json"

_money = dict()
_totalv = 1000000000
_frozen = _totalv
UNIT = "mE"

if exists(FILENAME):
    with open(FILENAME, "r") as file:
        data = load(file)
    _money = data["money"]
    _totalv = data["totalv"]
    _frozen = data["frozen"]


def get_money(user_id: int):
    return _money.get(user_id, 0)


def set_money(user_id, amount):
    _money[user_id] = amount
    _dump()


def rotate(value):
    delta = round(_frozen * (exp(value / _totalv) - 1))
    _frozen -= delta
    return delta


def freeze(self, amount: int) -> int:
    _frozen -= amount
    value = round(_totalv * log(amount / _frozen + 1))
    return value


def _dump():
    with open(FILENAME, "w") as file:
        dump({
            "money": _money,
            "totalv": _totalv,
            "frozen": _frozen,
        }, file)
