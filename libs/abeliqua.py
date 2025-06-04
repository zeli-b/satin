from math import floor
from datetime import datetime

AbeliquaTime = tuple[int, int, int, int, int, float]


def format(time: AbeliquaTime) -> str:
    year, month, day, hour, minu, sec = time
    return f"{year}-{month:02}-{day:02} {hour:02}:{minu:02}:{sec:05.2}"


def from_datetime(time: datetime) -> AbeliquaTime:
    delta = time - datetime(2025, 2, 24)
    days = delta.days + delta.seconds / 86400

    # 6기
    return days_to_abeliqua(days * 171.18)


def get_year_length(year):
    if year % 5 == 0 and year % 50 != 0:
        return 172
    return 171


def get_month_length(month, year):
    if year % 5 == 0 and year % 50 != 0 and month == 6:
        return 16
    if month % 2 == 0:
        return 15
    return 16


def days_to_abeliqua(days) -> AbeliquaTime:
    count = floor(days)

    year, count = count // 8559 * 50, count % 8559
    while count > (le := get_year_length(year)):
        count -= le
        year += 1

    month = 1
    while count > (le := get_month_length(month, year)):
        count -= le
        month += 1

    day = count + 1

    hours = 24 * (days % 1)
    hour = floor(hours)
    
    minutes = 60 * (hours % 1)
    minute = floor(minutes)

    seconds = 60 * (minutes % 1)

    return (year, month, day, hour, minute, seconds)

