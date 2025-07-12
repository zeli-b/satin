from math import floor
from datetime import datetime, timedelta

AbeliquaTime = tuple[int, int, int, int, int, float]


def format(time: AbeliquaTime) -> str:
    year, month, day, hour, minu, sec = time
    return f"{year}-{month:02}-{day:02} {hour:02}:{minu:02}:{sec:05.2f}"


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


def days_to_abeliqua(days: float) -> AbeliquaTime:
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


def abeliqua_to_days(time: AbeliquaTime) -> float:
    year, month, day, hour, minute, seconds = time

    total_days = 0.0

    # 1. 년도까지의 일수 계산 (50년 주기 8559일 활용)
    total_days += (year // 50) * 8559
    remaining_years = year % 50

    for y in range(remaining_years):
        total_days += get_year_length(y)

    # 2. 월까지의 일수 계산
    for m in range(1, month):
        total_days += get_month_length(m, year)

    # 3. 일수 추가 (day는 1부터 시작하므로 -1)
    total_days += (day - 1)

    # 4. 시간, 분, 초 추가
    total_days += hour / 24
    total_days += minute / (24 * 60)
    total_days += seconds / (24 * 60 * 60)

    return total_days


def to_datetime(abeliqua_time: AbeliquaTime) -> datetime:
    # 1. Abeliqua 시간을 기준일로부터의 총 일수로 변환
    abeliqua_total_days = abeliqua_to_days(abeliqua_time)

    # 2. Abeliqua 스케일 팩터를 역으로 적용하여 지구 일수 계산
    earth_days = abeliqua_total_days / 171.18

    # 3. 기준점 (2025년 2월 24일)에 지구 일수를 더하여 datetime 객체 생성
    base_datetime = datetime(2025, 2, 24)
    result_datetime = base_datetime + timedelta(days=earth_days)

    return result_datetime
