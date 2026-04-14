import uvicorn

from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from tests.demo_house import DEMO_HOUSE

from smarthouse.domain import Actuator, Measurement
from smarthouse.dto import SmartHouseInfo, FloorInfo, RoomInfo, DeviceInfo, ActuatorStateInfo

from pathlib import Path
import os
app = FastAPI()

smarthouse = DEMO_HOUSE

if not (Path.cwd() / "www").exists():
    os.chdir(Path.cwd().parent)
if (Path.cwd() / "www").exists():
    # http://localhost:8000/welcome/index.html
    app.mount("/static", StaticFiles(directory="www"), name="static")

# http://localhost:8000/ -> welcome page
@app.get("/")
def root():
    return RedirectResponse("/static/index.html")

# Health Check / Hello World
@app.get("/hello")
def hello(name: str = "world"):
    return {"hello": name}

#
# API endpoints for the smarthouse structural resources
#

@app.get("/smarthouse")
def get_smarthouse_info() -> SmartHouseInfo:
    """
    This endpoint returns an object that provides information
    about the general structure of the smarthouse.
    """
    return SmartHouseInfo.from_obj(smarthouse)


@app.get("/smarthouse/floor")
def get_floors() -> list[FloorInfo]:
    return [FloorInfo.from_obj(x) for x in smarthouse.get_floors()]

@app.get("/smarthouse/floor/{fid}")
def get_floor(fid: int) -> Response:
    for f in smarthouse.get_floors():
        if f.level == fid:
            return JSONResponse(content=jsonable_encoder(FloorInfo.from_obj(f)))
    return Response(status_code=404)

@app.get("/smarthouse/floor/{fid}/room")
def get_rooms(fid: int) -> list[RoomInfo]:

    # TODO

    return []


@app.get("/smarthouse/floor/{fid}/room/{rid}")
def get_room(fid: int, rid: int) -> Response:

    # TODO

    return Response(status_code=404)

@app.get("/smarthouse/device")
def get_devices() -> list[DeviceInfo]:

    # TODO

    return []

@app.get("/smarthouse/device/{uuid}")
def get_device(uuid: str) -> Response:

    # TODO

    return Response(status_code=404)

#
# API endpoints for sensors resources
#

@app.get("/smarthouse/sensor/{uuid}/current")
def read_measurement(uuid: str) -> Response:

    # TODO

    return Response(status_code=404)

@app.put("/smarthouse/sensor/{uuid}/current")
def update_sensor_measurement(uuid: str, measurement: Measurement) -> Response:

    # TODO

    return Response(status_code=404)

@app.delete("/smarthouse/sensor/{uuid}/current")
def delete_measurement(uuid: str) -> Response:

    # TODO

    return Response(status_code=404)

#
# API endpoints for actuator resources
#

@app.get("/smarthouse/actuator/{uuid}/state")
def read_actuator_state(uuid: str) -> Response:

    # TODO

    return Response(status_code=404)

@app.put("/smarthouse/actuator/{uuid}/state")
def update_sensor_state(uuid: str, target_state: ActuatorStateInfo) -> Response:

    # TODO

    return Response(status_code=404)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)