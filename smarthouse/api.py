import uvicorn

from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from tests.demo_house import DEMO_HOUSE

from smarthouse.domain import Actuator, Sensor
from smarthouse.dto import (
    SmartHouseInfo,
    FloorInfo,
    RoomInfo,
    DeviceInfo,
    ActuatorStateInfo,
    MeasurementInfo,
)

from pathlib import Path
import os

app = FastAPI()

smarthouse = DEMO_HOUSE

if not (Path.cwd() / "www").exists():
    os.chdir(Path.cwd().parent)
if (Path.cwd() / "www").exists():
    app.mount("/static", StaticFiles(directory="www"), name="static")


@app.get("/")
def root():
    return RedirectResponse("/static/index.html")


@app.get("/hello")
def hello(name: str = "world"):
    return {"hello": name}


#
# API endpoints for the smarthouse structural resources
#

@app.get("/smarthouse")
def get_smarthouse_info() -> SmartHouseInfo:
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
    for f in smarthouse.get_floors():
        if f.level == fid:
            return [RoomInfo.from_obj(r) for r in f.rooms]
    return []


@app.get("/smarthouse/floor/{fid}/room/{rid}")
def get_room(fid: int, rid: int) -> Response:
    for f in smarthouse.get_floors():
        if f.level == fid:
            for r in f.rooms:
                if getattr(r, "rid", None) == rid:
                    return JSONResponse(content=jsonable_encoder(RoomInfo.from_obj(r)))
    return Response(status_code=404)


@app.get("/smarthouse/device")
def get_devices() -> list[DeviceInfo]:
    return [DeviceInfo.from_obj(d) for d in smarthouse.get_devices()]


@app.get("/smarthouse/device/{uuid}")
def get_device(uuid: str) -> Response:
    device = smarthouse.get_device_by_id(uuid)
    if device is None:
        return Response(status_code=404)
    return JSONResponse(content=jsonable_encoder(DeviceInfo.from_obj(device)))


#
# API endpoints for sensor resources
#

@app.get("/smarthouse/sensor/{uuid}/current")
def read_measurement(uuid: str) -> Response:
    device = smarthouse.get_device_by_id(uuid)

    if device is None or not device.is_sensor():
        return Response(status_code=404)

    measurement = device.last_measurement()
    return JSONResponse(
        content=jsonable_encoder(
            {
                "timestamp": measurement.timestamp,
                "value": measurement.value,
                "unit": measurement.unit,
            }
        )
    )


@app.put("/smarthouse/sensor/{uuid}/current", response_model=None)
def update_sensor_measurement(uuid: str, measurement: MeasurementInfo) -> Response:
    device = smarthouse.get_device_by_id(uuid)

    if device is None or not device.is_sensor():
        return Response(status_code=404)

    device.add_measurement(value=measurement.value, unit=measurement.unit)
    return Response(status_code=204)


@app.delete("/smarthouse/sensor/{uuid}/oldest")
def delete_measurement(uuid: str) -> Response:
    device = smarthouse.get_device_by_id(uuid)

    if device is None or not device.is_sensor():
        return Response(status_code=404)

    measurements = device.get_measurements()
    if not measurements:
        return Response(status_code=404)

    device._measurements.pop(0)
    return Response(status_code=204)


#
# API endpoints for actuator resources
#

@app.get("/smarthouse/actuator/{uuid}/state")
def read_actuator_state(uuid: str) -> Response:
    device = smarthouse.get_device_by_id(uuid)

    if device is None or not device.is_actuator():
        return Response(status_code=404)

    state = ActuatorStateInfo(state=device.is_active())
    return JSONResponse(content=jsonable_encoder(state))


@app.put("/smarthouse/actuator/{uuid}/state", response_model=None)
def update_sensor_state(uuid: str, target_state: ActuatorStateInfo) -> Response:
    device = smarthouse.get_device_by_id(uuid)

    if device is None or not device.is_actuator():
        return Response(status_code=404)

    if target_state.state:
        device.turn_on()
    else:
        device.turn_off()

    return Response(status_code=204)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)