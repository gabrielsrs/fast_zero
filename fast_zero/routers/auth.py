from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import (
    create_access_token,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['users'])
Session = Annotated[Session, Depends(get_session)]
OAuth2From = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2From,
    session: Session,
):
    user = session.scalar(select(User).where(form_data.username == User.email))

    if not user:
        raise HTTPException(
            datail='Incorrect email or password',
            status_code=HTTPStatus.UNAUTHORIZED,
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            datail='Incorrect email or password',
            status_code=HTTPStatus.UNAUTHORIZED,
        )

    access_token = create_access_token({'sub': user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}
