"""
    Oversetter API (Bestemmer hvordan man oversetter mellom JSON og Python objekter)
    """

from __future__ import annotations
from typing import Literal

from pydantic import BaseModel
from smarthouse.domain import (
    Actuator,
    ActuatorWithSensor,
    Device,
    Floor,
    Room,
    Sensor,
    SmartHouse,
    Measurement,
)


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


    @staticmethod
    def from_obj(floor: Floor) -> "FloorInfo":
        return FloorInfo(
            fid=floor.level,
            rooms=[room.rid for room in floor.rooms]
        )


class RoomInfo(BaseModel):
    rid: int
    room_size: float
    room_name: str | None
    floor: int
    devices: list[str]

    @staticmethod
    def from_obj(room: Room) -> "RoomInfo":
        return RoomInfo(
            rid=room.rid,
            room_size=room.room_size,
            room_name=room.room_name,
            floor=room.floor.level,
            devices=[device.id for device in room.devices]
        )


class DeviceInfo(BaseModel):
    id: str
    device_name: str
    device_type: str
    category: Literal["sensor", "actuator", "actuator_with_sensor"]

    @staticmethod
    def from_obj(device: Device) -> "DeviceInfo":
        if isinstance(device, ActuatorWithSensor):
            category = "actuator_with_sensor"
        elif isinstance(device, Sensor):
            category = "sensor"
        elif isinstance(device, Actuator):
            category = "actuator"
        else:
            raise ValueError(f"Unknown device type: {type(device)}")

        return DeviceInfo(
            id=device.id,
            device_name=device.device_name,
            device_type=device.device_type,
            category=category
        )


class MeasurementInfo(BaseModel):
    timestamp: str
    value: float
    unit: str

    @staticmethod
    def from_obj(measurement: Measurement) -> "MeasurementInfo":
        return MeasurementInfo(
            timestamp=measurement.timestamp.isoformat() if hasattr(measurement.timestamp, "isoformat") else str(measurement.timestamp),
            value=measurement.value,
            unit=measurement.unit
        )


class ActuatorStateInfo(BaseModel):
    state: bool
    target_value: float | None = None

    @staticmethod
    def from_obj(actuator: Actuator) -> "ActuatorStateInfo":
        return ActuatorStateInfo(
            state=actuator.is_active(),
            target_value=actuator.target_value
        )