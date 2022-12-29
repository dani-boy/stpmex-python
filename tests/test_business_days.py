import datetime as dt

import pytest

from stpmex.business_days import (
    AMERICA_CANCUN,
    AMERICA_MEXICO_CITY,
    current_cdmx_time_zone,
    get_next_business_day,
    get_prior_business_day,
)


def test_get_next_business_day_weekday():
    # monday
    today = dt.datetime(2021, 2, 8)
    bd = get_next_business_day(today)
    # date should be the same because it is
    # a working day
    assert bd == dt.date(today.year, today.month, today.day)


def test_get_next_business_day_weekend():
    # saturday
    today = dt.date(2021, 2, 13)
    bd = get_next_business_day(today)
    # date should be moved to monday because
    # it is a weekend
    assert bd == dt.date(2021, 2, 15)


def test_get_next_business_day_holiday():
    # holiday
    today = dt.date(2021, 2, 1)
    bd = get_next_business_day(today)
    # date should be moved to tuesday because
    # it is a holiday
    assert bd == dt.date(2021, 2, 2)


def test_get_next_business_day_holiday_friday():
    # holiday on friday
    today = dt.date(2021, 1, 1)
    bd = get_next_business_day(today)
    # date should be moved to next monday because
    # it is a holiday
    assert bd == dt.date(2021, 1, 4)


def test_get_next_business_day_bank_holiday():
    today = dt.datetime(2021, 11, 2)
    bd = get_next_business_day(today)
    assert bd == dt.date(2021, 11, 3)

    today = dt.datetime(2021, 12, 12)
    bd = get_next_business_day(today)
    assert bd == dt.date(2021, 12, 13)

    today = dt.datetime(2021, 4, 1)
    bd = get_next_business_day(today)
    assert bd == dt.date(2021, 4, 5)  # holy week and weekend


def test_next_business_day_datetime_after_6_pm():
    today = dt.datetime(2022, 4, 19, 17, 59)
    bd = get_next_business_day(today)
    assert bd == dt.date(2022, 4, 19)

    today = dt.datetime(2022, 4, 19, 18, 0)
    bd = get_next_business_day(today)
    assert bd == dt.date(2022, 4, 20)

    today = dt.datetime(2022, 4, 19, 23, 59)
    bd = get_next_business_day(today)
    assert bd == dt.date(2022, 4, 20)

    today = dt.datetime(2022, 4, 20, 0)
    bd = get_next_business_day(today)
    assert bd == dt.date(2022, 4, 20)

    # friday afternoon
    today = dt.datetime(2022, 4, 22, 17, 59)
    bd = get_next_business_day(today)
    assert bd == dt.date(2022, 4, 22)

    today = dt.datetime(2022, 4, 22, 18, 0)
    bd = get_next_business_day(today)
    assert bd == dt.date(2022, 4, 25)


def test_get_prior_working_day_weekday():
    # tuesday
    today = dt.datetime(2021, 2, 9)
    bd = get_prior_business_day(today)
    # date should be monday
    assert bd == dt.date(2021, 2, 8)


def test_get_prior_working_day_weekend():
    # monday
    today = dt.datetime(2021, 2, 8)
    bd = get_prior_business_day(today)
    # date should be the past friday
    assert bd == dt.date(2021, 2, 5)


def test_get_prior_working_day_holiday():
    # yesterday was holiday
    today = dt.date(2021, 2, 2)
    bd = get_prior_business_day(today)
    # date should be the past friday because
    # it goes back to holiday and then weekend
    assert bd == dt.date(2021, 1, 29)


@pytest.mark.parametrize(
    'test_date,expected_timezone',
    [
        (dt.datetime(2022, 4, 2), AMERICA_MEXICO_CITY),
        (dt.datetime(2022, 4, 3), AMERICA_CANCUN),
        (dt.datetime(2022, 4, 8), AMERICA_CANCUN),
        (dt.datetime(2022, 10, 29), AMERICA_CANCUN),
        (dt.datetime(2022, 10, 30), AMERICA_MEXICO_CITY),
        (dt.datetime(2023, 1, 1), AMERICA_MEXICO_CITY),
        (dt.datetime(2023, 4, 1), AMERICA_MEXICO_CITY),
        (dt.datetime(2023, 4, 2), AMERICA_CANCUN),
        (dt.datetime(2023, 4, 3), AMERICA_CANCUN),
        (dt.datetime(2023, 10, 28), AMERICA_CANCUN),
        (dt.datetime(2023, 10, 29), AMERICA_MEXICO_CITY),
        (dt.datetime(2023, 12, 31), AMERICA_MEXICO_CITY),
    ],
)
def test_current_cdmx_time_zone(test_date, expected_timezone):
    timezone = current_cdmx_time_zone(test_date)
    assert timezone == expected_timezone
