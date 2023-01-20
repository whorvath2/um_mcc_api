from decimal import Decimal

from co.deability.um_mcc import person_finder, cost_calulator

minutes_per_year = int(60 * 2080)
MINUTES_PER_YEAR = Decimal(str(minutes_per_year) + ".00")
DOLLAR_PER_MIN_SALARY = MINUTES_PER_YEAR
FIFTY_SALARY = Decimal("50000.00")
WEIRD_SALARY = Decimal("10334.82")


def test_finds_persons_by_name():
    actual = list(person_finder.find_by_name("William"))
    assert len(actual) > 0

    filtered = list(
        filter(lambda item: item and item["name"] == "HORVATH II,WILLIAM", actual)
    )
    assert len(filtered) == 1
    only = filtered[0]
    assert only["salary"] == Decimal("130313.00")


def test_finds_persons_by_name_dept():
    actual = person_finder.find_by_name_dept(name="William", dept="ICPSR")
    assert len(actual) == 1


def test_does_not_find_non_existent_person_by_name():
    assert len(list(person_finder.find_by_name("foobar"))) == 0


def test_calculates_per_minute_cost_correctly():
    assert cost_calulator.calc_per_min_cost(salary=DOLLAR_PER_MIN_SALARY) == Decimal(
        "1.00"
    )


def test_calculates_meeting_cost_correctly():
    salaries = [DOLLAR_PER_MIN_SALARY, DOLLAR_PER_MIN_SALARY, DOLLAR_PER_MIN_SALARY]
    mtg_len = 1
    expected = len(salaries)
    actual = cost_calulator.calc_meeting_cost(salaries=salaries, minutes=mtg_len)
    assert actual == expected

    mtg_len = 60
    expected = mtg_len * len(salaries)
    actual = cost_calulator.calc_meeting_cost(salaries=salaries, minutes=mtg_len)
    assert actual == expected

    per_min_fifty = round(FIFTY_SALARY / MINUTES_PER_YEAR, 2)
    salaries = [FIFTY_SALARY]
    expected = round(mtg_len * per_min_fifty, 2)
    actual = cost_calulator.calc_meeting_cost(salaries=salaries, minutes=mtg_len)
    assert actual == expected

    per_min_weird = round(WEIRD_SALARY / MINUTES_PER_YEAR, 2)
    salaries = [WEIRD_SALARY]
    expected = round(mtg_len * per_min_weird, 2)
    actual = cost_calulator.calc_meeting_cost(salaries=salaries, minutes=mtg_len)
    assert actual == expected

    salaries = [DOLLAR_PER_MIN_SALARY, FIFTY_SALARY, WEIRD_SALARY]
    per_min = per_min_weird + per_min_fifty + 1
    expected = round(per_min * mtg_len, 2)
    actual = cost_calulator.calc_meeting_cost(salaries=salaries, minutes=int(mtg_len))
    assert actual == expected
