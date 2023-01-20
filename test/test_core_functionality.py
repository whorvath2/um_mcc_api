from decimal import Decimal

from co.deability.um_mcc import person_finder, cost_calulator

DOLLAR_PER_MIN_SALARY = Decimal("124800")


def test_finds_persons_by_name():
    assert person_finder.find_by_name("William")


def test_does_not_find_non_existent_person_by_name():
    assert len(list(person_finder.find_by_name("foobar"))) == 0


def test_calculates_per_minute_cost_correctly():
    assert cost_calulator.calc_per_min_cost(salary=DOLLAR_PER_MIN_SALARY) == Decimal(
        "1.00"
    )


def test_calculates_meeting_cost_correctly():
    salaries = [DOLLAR_PER_MIN_SALARY, DOLLAR_PER_MIN_SALARY, DOLLAR_PER_MIN_SALARY]
    assert cost_calulator.calc_meeting_cost(salaries=salaries, minutes=1) == len(
        salaries
    )
    assert cost_calulator.calc_meeting_cost(salaries=salaries, minutes=60) == 60 * len(
        salaries
    )
