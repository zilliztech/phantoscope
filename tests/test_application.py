import pytest
from test_basic import client


def test_get_application_list(client):
    rv = client.get("/v1/application/")
    assert rv.status_code == 200
