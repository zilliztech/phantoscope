import pytest
from test_basic import client


def test_get_pipeline(client):
    rv = client.get("/v1/pipeline/")
    assert rv.status_code == 200
