from sanic import Sanic
from sanic.response import json

from auth import protected
from login import login


app = Sanic("AuthApp")
app.config.SECRET = "KEEP_IT_SECRET_KEEP_IT_SAFE"
app.blueprint(login)


@app.get("/")
async def hello_world(request):
    return json({"msg": "Hello, world."})


@app.get("/secret")
@protected
async def secret(request):
    return json({"msg": "To go fast, you must be fast."})

