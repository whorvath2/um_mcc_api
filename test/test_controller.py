import json
from decimal import Decimal
from http import HTTPStatus
from typing import Dict, Final

from co.deability.um_mcc import cost_calculator

ROOT: Final[str] = "/um_mcc"
FIND: Final[str] = f"{ROOT}/find"
COST: Final[str] = f"{ROOT}/cost"
ACCEPT_JSON_HEADERS: Final[Dict[str, str]] = {"Accept": "application/json"}
CONTENT_JSON_HEADERS: Final[Dict[str, str]] = {"Content-Type": "application/json"}


def test_health_check(http_client):
    with http_client:
        endpoint = f"{ROOT}"
        response = http_client.get(endpoint, headers=ACCEPT_JSON_HEADERS)
        assert response.status_code == HTTPStatus.OK
        assert response.json.get("status") == "OK"


def test_find_people_happy_and_sad_paths(http_client):
    with http_client:
        endpoint = f"{FIND}?name=William"
        response = http_client.get(endpoint, headers=ACCEPT_JSON_HEADERS)
        assert response.status_code == HTTPStatus.OK
        assert len(response.json) > 100

        endpoint = f"{FIND}?name=Foobar"
        response = http_client.get(endpoint, headers=ACCEPT_JSON_HEADERS)
        assert response.status_code == HTTPStatus.OK
        assert response.json == []


def test_calculate_meeting_cost(http_client):
    with http_client:
        endpoint = f"{FIND}?name=William"
        bills = http_client.get(endpoint, headers=ACCEPT_JSON_HEADERS).json
        assert bills
        mtg_minutes = Decimal("20.00")
        running_total = Decimal("0.00")
        for bill in bills:
            per_min = cost_calculator.calc_per_min_cost(bill["salary"])
            total = mtg_minutes * per_min
            running_total = round(running_total + total, 2)

        endpoint = f"{COST}/{int(mtg_minutes)}"
        response = http_client.post(
            endpoint,
            headers=ACCEPT_JSON_HEADERS | CONTENT_JSON_HEADERS,
            json=json.dumps(bills),
        )
        assert response.status_code == HTTPStatus.OK
        # actual = str(response.text).strip('\n"')
        actual = json.loads(response.text)
        expected = json.loads('{"cost": "' + str(running_total) + '"}')
        assert actual == expected

        # SAD PATH
        endpoint = f"{FIND}?name=foobar"
        bills = http_client.get(endpoint, headers=ACCEPT_JSON_HEADERS).json
        assert len(bills) == 0
        endpoint = f"{COST}/{int(mtg_minutes)}"
        response = http_client.post(
            endpoint,
            headers=ACCEPT_JSON_HEADERS | CONTENT_JSON_HEADERS,
            json=json.dumps(bills),
        )
        assert response.status_code == HTTPStatus.OK
        actual = json.loads(response.text)
        assert int(actual["cost"]) == 0

        # todo make the controller raise an error if no matching names are found
