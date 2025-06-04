from json import load, dump

FILENAME = "res/memo.json"
try:
    with open(FILENAME, "r") as file:
        _data = load(file)
except:
    _data = dict()


def get_memo(name):
    return _data.get(name, "")


def set_memo(memo, content):
    if content:
        _data[memo] = content
        return

    del _data[memo]
    _save()


def get_memo_list():
    return list(_data.keys())


def _save():
    with open(FILENAME, "w") as file:
        dump(_data, file, ensure_ascii=False)
