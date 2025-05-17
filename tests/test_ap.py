from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_return_hii():
    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Hii'}
    assert response.status_code == HTTPStatus.OK
