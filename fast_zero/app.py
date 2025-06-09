from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routers import auth, users
from fast_zero.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Hii'}


@app.get('/a2', response_class=HTMLResponse)
def a2():
    return '<h1>ola mundo</h1>'
