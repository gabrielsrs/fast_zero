from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Hii'}


@app.get('/a2', response_class=HTMLResponse)
def a2():
    return '<h1>ola mundo</h1>'
