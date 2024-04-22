# autopep8: off
import os
import uvicorn
from typing import Literal
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from lib.httpio import HttpOutMiddleware
from lib.log import load_log_config
import database.tinydb_driver as tdb
import lib.mqtt as mqtt
from dotenv import load_dotenv
load_dotenv()

# routes
from routes import auth_api
from routes import rooms_api
from routes import devices_api
from routes import scenes_api
# autopep8: on


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init app
    tdb.tinydb_init()
    mqtt.mqtt_connect()
    yield
    # clean up resources here
    mqtt.mqtt_disconnect()

server = FastAPI(
    title='ISI Server',
    description='Added ISI-V2 Core Modules',
    version='3.0.1',
    lifespan=lifespan,
)

server.add_middleware(HttpOutMiddleware)
server.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

server.include_router(auth_api.router)
server.include_router(rooms_api.router)
server.include_router(devices_api.router)
server.include_router(scenes_api.router)


@server.get(f"{os.environ['API_ROOT']}/test")
async def get_test() -> Literal['server online'] | None:
    """Test route to check if server is online."""
    return JSONResponse(content='SERVER_ONLINE')


if __name__ == '__main__':
    load_log_config()
    uvicorn.run(server, host='0.0.0.0', port=8080)
