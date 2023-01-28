from http import HTTPStatus
from typing import Dict, Final

ROOT: Final[str] = "/um_mcc"
FIND: Final[str] = f"{ROOT}/find"
ACCEPT_JSON_HEADERS: Final[Dict[str, str]] = {"Accept": "application/json"}


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
