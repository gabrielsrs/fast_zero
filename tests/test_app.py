from http import HTTPStatus


def test_root_return_hii(client):
    response = client.get('/')

    assert response.json() == {'message': 'Hii'}
    assert response.status_code == HTTPStatus.OK


def test_a2(client):
    response = client.get('/a2')

    assert response.text == '<h1>ola mundo</h1>'
    assert response.status_code == HTTPStatus.OK
