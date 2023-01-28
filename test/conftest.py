import os
import sys

import pytest

# add the parent directory to the path per noqa: E402
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")


@pytest.fixture
def start_app():
    from co.deability.um_mcc import app

    test_app = app.init_app()
    test_app.testing = True
    test_app.debug = True
    print(test_app.url_map)
    with test_app.app_context():
        yield test_app


@pytest.fixture
def http_client(start_app):
    """
    Mock HTTP client for use in testing blueprint routes.
    """
    with start_app.app_context():
        client = start_app.test_client()
        yield client
