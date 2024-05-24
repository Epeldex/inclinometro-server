import os
import threading

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel
from starlette.middleware.gzip import GZipMiddleware
from starlette.templating import Jinja2Templates
    
from mainClient import getDevicesFromServer, refreshData, stopService, swapDevices


app = FastAPI()

env = Environment(
    loader=FileSystemLoader(os.path.abspath("Cliente/templates/")),
    autoescape=select_autoescape()
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return env.get_template("index.html").render()


@app.get("/devices")
async def coms_root():
    return getDevicesFromServer()

@app.get("/select_device/{device_name}")
async def select_device(device_name):
    if device_name is not None and device_name[:3] == "LAN":
        swapDevices(device_name)
    else:
        stopService()
        
@app.get("/refresh_data/{device_name}")
async def refresh_Data(device_name):
    return refreshData(device_name)