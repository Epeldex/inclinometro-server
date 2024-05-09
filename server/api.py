import os
import threading

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel
from starlette.middleware.gzip import GZipMiddleware
from starlette.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(GZipMiddleware, minimum_size=500)

templates = Jinja2Templates(directory=os.path.abspath("../templates"))

env = Environment(
    loader=FileSystemLoader(os.path.abspath("../templates")),
    autoescape=select_autoescape()
)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    template = env.get_template("index.html")
    return templates.TemplateResponse("index.html", {"request": request})
