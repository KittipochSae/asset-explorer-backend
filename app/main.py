from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis
import config
import utils

import json
import numpy as np


app = FastAPI()
origins = [
    "http://localhost",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

r = redis.StrictRedis(host=config.REDIS_URL, port=config.REDIS_PORT,
                      password=config.REDIS_AUTH, db=0, socket_timeout=None)


utils.load_data(r)


@app.get("/")
async def root():
    return {"message": "Welcome to map service"}


@app.get("/map")
async def map(left: float, right: float, top: float, bottom: float, zoom: int):
    if zoom <= 12:
        i = 0
    if zoom == 13:
        i = 1
    if zoom == 14:
        i = 2
    if zoom == 15:
        i = 3
    if zoom >= 16:
        i = 4
    json_landpoints = []
    _left = int(left/config.BIG_GRID_WIDTH[i]) * \
        config.BIG_GRID_WIDTH[i]-config.BIG_GRID_WIDTH[i]
    _right = int(right/config.BIG_GRID_WIDTH[i]) * \
        config.BIG_GRID_WIDTH[i]+config.BIG_GRID_WIDTH[i]
    _top = int(top/config.BIG_GRID_WIDTH[i]) * \
        config.BIG_GRID_WIDTH[i]+config.BIG_GRID_WIDTH[i]
    _bottom = int(bottom/config.BIG_GRID_WIDTH[i]) * \
        config.BIG_GRID_WIDTH[i]-config.BIG_GRID_WIDTH[i]
    for lat in np.arange(_bottom, _top + config.BIG_GRID_WIDTH[i], config.BIG_GRID_WIDTH[i]):
        for lon in np.arange(_left, _right + config.BIG_GRID_WIDTH[i], config.BIG_GRID_WIDTH[i]):
            res = r.get(
                f"landpoint-{i}-{'{:.5f}'.format(lat)}-{'{:.5f}'.format(lon)}")
            if res is not None:
                json_landpoints = json_landpoints + \
                    json.loads(res, parse_float=lambda x: round(float(x), 6))
    return json_landpoints


@app.get("/grid")
async def grid(left: float, right: float, top: float, bottom: float, zoom: int):
    if zoom <= 12:
        i = 0
    if zoom == 13:
        i = 1
    if zoom == 14:
        i = 2
    if zoom == 15:
        i = 3
    if zoom >= 16:
        i = 4
    json_grids = []
    _left = int(left/config.BIG_GRID_WIDTH[i]) * \
        config.BIG_GRID_WIDTH[i]-config.BIG_GRID_WIDTH[i]
    _right = int(right/config.BIG_GRID_WIDTH[i]) * \
        config.BIG_GRID_WIDTH[i]+config.BIG_GRID_WIDTH[i]
    _top = int(top/config.BIG_GRID_WIDTH[i]) * \
        config.BIG_GRID_WIDTH[i]+config.BIG_GRID_WIDTH[i]
    _bottom = int(bottom/config.BIG_GRID_WIDTH[i]) * \
        config.BIG_GRID_WIDTH[i]-config.BIG_GRID_WIDTH[i]
    for lat in np.arange(_bottom, _top + config.BIG_GRID_WIDTH[i], config.BIG_GRID_WIDTH[i]):
        for lon in np.arange(_left, _right + config.BIG_GRID_WIDTH[i], config.BIG_GRID_WIDTH[i]):
            res = r.get(
                f"grid-{i}-{'{:.5f}'.format(lat)}-{'{:.5f}'.format(lon)}")
            if res is not None:
                json_grids = json_grids + \
                    json.loads(res, parse_float=lambda x: round(float(x), 6))
    return json_grids
