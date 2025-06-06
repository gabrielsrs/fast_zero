from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_return_hii(client):
    response = client.get('/')

    assert response.json() == {'message': 'Hii'}
    assert response.status_code == HTTPStatus.OK


def test_a2(client):
    response = client.get('/a2')

    assert response.text == '<h1>ola mundo</h1>'
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'alice@123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
    }


def test_read_users_without_user(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'bob@123',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@example.com',
    }


def test_update_not_found_user_id(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'angelico',
            'email': 'angelico@example.com',
            'password': 'angelico@123',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'user_id=2 not found'}


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@example.com',
    }


def test_read_not_found_user(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'user_id=2 not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_not_found_user(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'user_id=2 not found'}


def test_update_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'Jhon Doe',
            'email': 'jhon@email.com',
            'password': 'jhon@123',
        },
    )

    response = client.put(
        f'users/{user.id}',
        json={
            'username': 'Jhon Doe',
            'email': 'jhon@email.com',
            'password': 'jhon@123',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exist'}
