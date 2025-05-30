from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app

client = TestClient(app)


def test_root_return_hii():
    response = client.get('/')

    assert response.json() == {'message': 'Hii'}
    assert response.status_code == HTTPStatus.OK


def test_a2():
    response = client.get('/a2')

    assert response.text == '<h1>ola mundo</h1>'
    assert response.status_code == HTTPStatus.OK
