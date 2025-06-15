from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.models import User
from tests.test_todo import TodoFactory


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username='test', email='test@test', password='test')

        session.add(new_user)
        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == 'test')
        )

        assert asdict(user) == {
            'id': 1,
            'username': 'test',
            'email': 'test@test',
            'password': 'test',
            'updated_at': time,
            'created_at': time,
            'todos': [],
        }


@pytest.mark.asyncio
async def test_value_out_of_state_values(session: AsyncSession, user):
    todo = TodoFactory(user_id=user.id, state='Test')

    session.add(todo)
    await session.commit()

    with pytest.raises(LookupError) as error:
        await session.refresh(todo)

    assert error.type is LookupError
