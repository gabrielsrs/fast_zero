import asyncio
import sys

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routers import auth, todos, users
from fast_zero.schemas import Message

if sys.platform == 'wen32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get('/', response_model=Message)
async def read_root():
    return {'message': 'Hii'}


@app.get('/a2', response_class=HTMLResponse)
async def a2():
    return '<h1>ola mundo</h1>'
