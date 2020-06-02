import pytest
from test_basic import client


class TestApplicationApi:
    """test class for application api"""
    name = "pytestexample"

    def test_get_application_list(self, client):
        rv = client.get("/v1/application/")
        assert rv.status_code == 200
