from datetime import datetime, timedelta
from json import load, dump

FILENAME = "res/attend.json"

try:
    with open(FILENAME, "r") as file:
        _data = load(file)
except:
    _data = dict()


def attend(user_id):
    today = datetime.today().isoformat()
    yesterday = (datetime.today() - timedelta(days=1)).isoformat()

    day, streak = _data.get(str(user_id), [yesterday, 0])

    if day != yesterday:
        day = today
        streak = 1
    else:
        day = today
        streak += 1

    _data[str(user_id)] = [day, streak]
    _save()

    return streak


def _save():
    with open(FILENAME, "w") as file:
        dump(_data, file)
