from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token


def test_jwt(settings):
    data = {'test': 'test'}

    token = create_access_token(data)
    decoded = decode(token, settings.SECRET_KEY, settings.ALGORITHM)

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_not_sub_in_jwt(client):
    data = {'test': 'test'}

    token = create_access_token(data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_not_user_to_email(client):
    data = {'sub': 'test@email.com'}

    token = create_access_token(data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
