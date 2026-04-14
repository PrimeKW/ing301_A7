from __future__ import annotations
from typing import Literal

from pydantic import BaseModel
from smarthouse.domain import Actuator, ActuatorWithSensor, Device, Floor, Room, Sensor, SmartHouse


class SmartHouseInfo(BaseModel):
    no_rooms: int
    no_floors: int
    total_area: float
    no_devices: int

    @staticmethod
    def from_obj(house: SmartHouse) -> "SmartHouseInfo":
        return SmartHouseInfo(
            no_rooms=len(house.get_rooms()),
            no_floors=len(house.get_floors()),
            total_area=house.get_area(),
            no_devices=len(house.get_devices())
        )


class FloorInfo(BaseModel):
    fid: int
    rooms: list[int]

    @staticmethod
    def from_obj(floor: Floor) -> "FloorInfo":
        return FloorInfo(
            fid=floor.level,
            rooms=[r.rid for r in floor.rooms if hasattr(r, "rid")]
        )


class RoomInfo(BaseModel):
    rid: int | None
    room_size: float
    room_name: str | None
    floor: int
    devices: list[str]

    @staticmethod
    def from_obj(room: Room) -> "RoomInfo":
        return RoomInfo(
            rid=getattr(room, "rid", None),
            room_size=room.room_size,
            room_name=room.room_name,
            floor=room.floor.level,
            devices=[device.id for device in room.devices]
        )


class DeviceInfo(BaseModel):
    id: str
    device_name: str
    device_type: Literal["sensor", "actuator", "actuator_with_sensor"]

    @staticmethod
    def from_obj(device: Device) -> "DeviceInfo":
        if isinstance(device, ActuatorWithSensor):
            dtype = "actuator_with_sensor"
        elif isinstance(device, Sensor):
            dtype = "sensor"
        elif isinstance(device, Actuator):
            dtype = "actuator"
        else:
            raise ValueError(f"Unknown device type: {type(device)}")

        return DeviceInfo(
            id=device.id,
            device_name=device.device_name,
            device_type=dtype
        )

class MeasurementInfo(BaseModel):
    timestamp: str | None = None
    value: float
    unit: str


class ActuatorStateInfo(BaseModel):
    state: bool