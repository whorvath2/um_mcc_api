from decimal import Decimal
from typing import Final, List

MINUTES_PER_YEAR: Final[Decimal] = Decimal("2080") * Decimal("60")


def calc_per_min_cost(salary: Decimal) -> Decimal:
    return salary / MINUTES_PER_YEAR


def calc_attendee_cost(salary: Decimal, minutes: int) -> Decimal:
    return calc_per_min_cost(salary=salary) * minutes


def calc_meeting_cost(salaries: List[Decimal], minutes: int) -> Decimal:
    return sum(
        [calc_attendee_cost(salary=salary, minutes=minutes) for salary in salaries]
    )
