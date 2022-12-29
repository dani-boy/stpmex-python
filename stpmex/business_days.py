import datetime as dt
from itertools import count
from typing import Union

from workalendar.america import Mexico

# Day numbers taken from
# https://docs.python.org/3.8/library/datetime.html#datetime.date.weekday
MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

WEEKEND = {SATURDAY, SUNDAY}

AMERICA_MEXICO_CITY = 'America/Mexico_City'
AMERICA_CANCUN = 'America/Cancun'

# It is possible to calculate the exact days for holy week, but
# it requires to integrate a astronomical calendar
# package library. For simplicity we use calculated dates in next
# 5 years
HOLY_WEEKS_PER_YEAR = {
    2021: (dt.date(2021, 4, 1), dt.date(2021, 4, 4)),
    2022: (dt.date(2022, 4, 14), dt.date(2022, 4, 17)),
    2023: (dt.date(2023, 4, 6), dt.date(2023, 4, 9)),
    2024: (dt.date(2024, 3, 28), dt.date(2024, 3, 31)),
    2025: (dt.date(2025, 4, 17), dt.date(2025, 4, 20)),
    2026: (dt.date(2026, 4, 2), dt.date(2026, 4, 5)),
}


def get_next_business_day(fecha: Union[dt.datetime, dt.date]) -> dt.date:
    """
    Obtains the next business day in case the current one is not.
    """
    try:
        # based on
        # https://stpmex.zendesk.com/hc/es/articles/360045884491-Fecha-de-Operaci%C3%B3n
        assert fecha.hour >= 18
        fecha = fecha.date() + dt.timedelta(days=1)
    except (AssertionError, AttributeError):
        ...

    mx = Mexico()
    holidays = [hol[0] for hol in mx.holidays(fecha.year)]

    holy_week_begin, holy_week_end = HOLY_WEEKS_PER_YEAR[fecha.year]

    holy_week = [
        holy_week_begin + dt.timedelta(days=n)
        for n in range(int((holy_week_end - holy_week_begin).days) + 1)
    ]
    bank_holiday = holy_week + [
        dt.date(fecha.year, 11, 2),
        dt.date(fecha.year, 12, 12),
    ]
    holidays += bank_holiday

    business_day = dt.date(fecha.year, fecha.month, fecha.day)
    while business_day.weekday() in WEEKEND or business_day in holidays:
        business_day = business_day + dt.timedelta(days=1)

    return business_day


def get_prior_business_day(fecha: Union[dt.datetime, dt.date]) -> dt.date:
    """
    Obtains the previous business day.
    """
    mx = Mexico()
    holidays = [hol[0] for hol in mx.holidays(fecha.year)]
    business_day = dt.date(fecha.year, fecha.month, fecha.day)

    business_day = business_day - dt.timedelta(days=1)
    while business_day.weekday() in WEEKEND or business_day in holidays:
        business_day = business_day - dt.timedelta(days=1)

    return business_day


# based on
# http://www.dof.gob.mx/nota_detalle.php?codigo=4864678&fecha=04/01/1996
def current_cdmx_time_zone(fecha: dt.datetime) -> str:
    april = dt.datetime(fecha.year, 4, 1)
    october = dt.datetime(fecha.year, 10, 31)

    days = (april + dt.timedelta(days=i) for i in count())
    april_first_sunday = next(day for day in days if day.weekday() == SUNDAY)

    days = (october - dt.timedelta(days=i) for i in count())
    october_last_sunday = next(day for day in days if day.weekday() == SUNDAY)

    if april_first_sunday <= fecha < october_last_sunday:
        return AMERICA_CANCUN
    else:
        return AMERICA_MEXICO_CITY
