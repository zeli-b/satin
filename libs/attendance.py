from datetime import date, timedelta
from json import load, dump

FILENAME = "res/attend.json"

try:
    with open(FILENAME, "r") as file:
        _data = load(file)
except:
    _data = dict()


def attend(user_id):
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    row = _data.get(str(user_id), [yesterday, 0, 0])
    day = row[0] if len(row) > 0 else yesterday
    streak = row[1] if len(row) > 1 else 0
    record = row[2] if len(row) > 2 else 0

    if day == today:
        return 0

    if day != yesterday:
        day = today
        streak = 1
    else:
        day = today
        streak += 1

    _data[str(user_id)] = [day, streak, min(streak, record)]
    _save()

    return streak


def get_record(user_id: int):
    key = str(user_id)
    if len(_data[key]) <= 2:
        return _data[key][1]
    return _data[key][2]


def _save():
    with open(FILENAME, "w") as file:
        dump(_data, file)
