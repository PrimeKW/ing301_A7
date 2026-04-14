from __future__ import annotations
from typing import Literal

from pydantic import BaseModel
from smarthouse.domain import Actuator, ActuatorWithSensor, Device, Floor, Room, Sensor, SmartHouse

"""
Classes for data transfer in the cloud service API endpoints between
what is sent/received int eh API and the data stored in the object structure
representing the smart house using the underlying domain model
"""

class SmartHouseInfo(BaseModel):

    no_rooms: int
    no_floors: int
    total_area: float
    no_devices: int

    @staticmethod
    def from_obj(house: SmartHouse) -> SmartHouseInfo:
        return SmartHouseInfo(
            no_rooms=len(house.get_rooms()),
            no_floors=len(house.get_floors()),
            total_area=house.get_area(),
            no_devices=len(house.get_devices()))


class FloorInfo(BaseModel):

    fid: int
    rooms: list[int]

    @staticmethod
    def from_obj(floor: Floor) -> FloorInfo:
        return FloorInfo(
            fid=floor.level,
            rooms=[r.rid for r in floor.rooms]
        )

class RoomInfo(BaseModel):

    rid: int | None
    room_size: float
    room_name: str | None
    floor: int
    devices: list[str]

    @staticmethod
    def from_obj(room: Room) -> RoomInfo:

        # TODO
        pass

class DeviceInfo(BaseModel):

    # TODO

    @staticmethod
    def from_obj(device: Device) -> DeviceInfo:

        # TODO
        pass

class ActuatorStateInfo(BaseModel):

    # TODO
    pass