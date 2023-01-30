from decimal import Decimal

import pytest

from co.deability.um_mcc import cost_calculator, person_finder

minutes_per_year = int(60 * 2080)
MINUTES_PER_YEAR = Decimal(str(minutes_per_year) + ".00")
DOLLAR_PER_MIN_SALARY = MINUTES_PER_YEAR
FIFTY_SALARY = Decimal("50000.00")
WEIRD_SALARY = Decimal("10334.82")


def test_finds_persons_by_name():
    args = {"name": "William"}
    actual = person_finder.find(args)
    assert len(actual) > 0
    filtered = list(
        filter(lambda item: item and item["name"] == "HORVATH II,WILLIAM", actual)
    )
    assert len(filtered) == 1
    only = filtered[0]
    assert only["salary"] == Decimal("130313.00")


def test_finds_persons_by_name_dept():
    args = {"name": "William", "department": "ICPSR"}
    actual = person_finder.find(args)
    assert len(actual) == 1


def test_finds_persons_by_name_title():
    args = {"name": "William", "title": "App Programming"}
    actual = person_finder.find(args)
    assert len(actual) == 1


def test_does_not_find_person_when_title_or_dept_is_wrong():
    args = {"name": "William", "title": "foobar"}
    actual = person_finder.find(args)
    assert len(actual) == 0

    args = {"name": "William", "department": "foobar"}
    actual = person_finder.find(args)
    assert len(actual) == 0

    args = {"name": "William", "department": "ICPSR", "title": "foobar"}
    actual = person_finder.find(args)
    assert len(actual) == 0


def test_fails_without_name():
    with pytest.raises(KeyError):
        actual = person_finder.find({})

    with pytest.raises(KeyError):
        args = {"department": "ICPSR", "title": "App Programming"}
        actual = person_finder.find(args)


def test_does_not_find_non_existent_person_by_name():
    args = {"name": "foobar"}
    assert len(list(person_finder.find(args))) == 0


def test_calculates_per_minute_cost_correctly():
    assert cost_calculator.calc_per_min_cost(salary=DOLLAR_PER_MIN_SALARY) == Decimal(
        "1.00"
    )


def test_calculates_meeting_cost_correctly():
    salaries = [DOLLAR_PER_MIN_SALARY, DOLLAR_PER_MIN_SALARY, DOLLAR_PER_MIN_SALARY]
    mtg_len = 1
    expected = len(salaries)
    actual = cost_calculator.calc_meeting_cost(salaries=salaries, minutes=mtg_len)
    assert actual == expected

    mtg_len = 60
    expected = mtg_len * len(salaries)
    actual = cost_calculator.calc_meeting_cost(salaries=salaries, minutes=mtg_len)
    assert actual == expected

    per_min_fifty = round(FIFTY_SALARY / MINUTES_PER_YEAR, 2)
    salaries = [FIFTY_SALARY]
    expected = round(mtg_len * per_min_fifty, 2)
    actual = cost_calculator.calc_meeting_cost(salaries=salaries, minutes=mtg_len)
    assert actual == expected

    per_min_weird = round(WEIRD_SALARY / MINUTES_PER_YEAR, 2)
    salaries = [WEIRD_SALARY]
    expected = round(mtg_len * per_min_weird, 2)
    actual = cost_calculator.calc_meeting_cost(salaries=salaries, minutes=mtg_len)
    assert actual == expected

    salaries = [DOLLAR_PER_MIN_SALARY, FIFTY_SALARY, WEIRD_SALARY]
    per_min = per_min_weird + per_min_fifty + 1
    expected = round(per_min * mtg_len, 2)
    actual = cost_calculator.calc_meeting_cost(salaries=salaries, minutes=int(mtg_len))
    assert actual == expected
