from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Hii'}


@app.get('/a2', response_class=HTMLResponse)
def a2():
    return '<h1>ola mundo</h1>'


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            detail=f'{user_id=} not found', status_code=HTTPStatus.NOT_FOUND
        )

    return database[user_id - 1]


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(offset).limit(limit))
    return {'users': users}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                detail='Username already exist',
                status_code=HTTPStatus.CONFLICT,
            )

        if db_user.email == user.email:
            raise HTTPException(
                detail='Email already exist', status_code=HTTPStatus.CONFLICT
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user: UserSchema, user_id: int, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            detail='User not found', status_code=HTTPStatus.NOT_FOUND
        )

    try:
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user
    except IntegrityError:
        raise HTTPException(
            detail='Username or Email already exist',
            status_code=HTTPStatus.CONFLICT,
        )


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            detail='User not found', status_code=HTTPStatus.NOT_FOUND
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}
