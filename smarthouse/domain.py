from __future__ import annotations

from datetime import datetime
from typing import Optional


class Measurement:
    def __init__(self, timestamp: datetime, value: float, unit: str):
        self.timestamp = timestamp
        self.value = float(value)
        self.unit = str(unit)


"""Etasje og rom"""


class Floor:
    def __init__(self, level: int):
        self.level = int(level)
        self.rooms: list[Room] = []

    def add_room(self, room: "Room") -> None:
        if room not in self.rooms:
            self.rooms.append(room)


class Room:
    _next_id = 1

    def __init__(self, floor: Floor, room_size: float, room_name: Optional[str] = None):
        self.rid = Room._next_id
        Room._next_id += 1

        self.floor = floor
        self.room_size = float(room_size)
        self.room_name = room_name
        self.devices: list[Device] = []

    def add_device(self, device: "Device") -> None:
        if device not in self.devices:
            self.devices.append(device)

    def remove_device(self, device: "Device") -> None:
        if device in self.devices:
            self.devices.remove(device)


"""Enheter"""


class Device:
    def __init__(self, id: str, device_type: str, device_name: str, supplier: str):
        self.id = str(id)
        self.device_type = str(device_type)
        self.device_name = str(device_name)
        self.model_name = str(device_name)
        self.supplier = str(supplier)
        self.room: Optional[Room] = None

    def is_actuator(self) -> bool:
        return False

    def is_sensor(self) -> bool:
        return False

    def get_device_type(self) -> str:
        return self.device_type


class Sensor(Device):
    def __init__(
        self,
        id: str,
        device_type: str,
        device_name: str,
        supplier: str,
        unit: Optional[str] = None
    ):
        super().__init__(id, device_type, device_name, supplier)
        self.unit = unit
        self._measurements: list[Measurement] = []

    def is_sensor(self) -> bool:
        return True

    def add_measurement(
        self,
        value: float,
        unit: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> Measurement:
        if unit is None:
            if self.unit is None:
                raise ValueError("Unit må oppgis første gang, eller være satt på sensoren.")
            unit = self.unit
        else:
            self.unit = unit

        if timestamp is None:
            timestamp = datetime.now()

        measurement = Measurement(timestamp, value, unit)
        self._measurements.append(measurement)
        return measurement

    def last_measurement(self) -> Optional[Measurement]:
        if not self._measurements:
            return None
        return self._measurements[-1]

    def get_measurements(self) -> list[Measurement]:
        return list(self._measurements)

    def remove_current_measurement(self) -> Optional[Measurement]:
        if not self._measurements:
            return None
        return self._measurements.pop()

    def clear_measurements(self) -> None:
        self._measurements.clear()


class Actuator(Device):
    def __init__(self, id: str, device_type: str, device_name: str, supplier: str):
        super().__init__(id, device_type, device_name, supplier)
        self._active = False
        self.target_value: Optional[float] = None

    def is_actuator(self) -> bool:
        return True

    def turn_on(self, target_value: Optional[float] = None) -> None:
        self._active = True
        if target_value is not None:
            self.target_value = float(target_value)

    def turn_off(self) -> None:
        self._active = False
        self.target_value = None

    def is_active(self) -> bool:
        return self._active

    def set_state(self, active: bool, target_value: Optional[float] = None) -> None:
        if active:
            self.turn_on(target_value)
        else:
            self.turn_off()


class ActuatorWithSensor(Actuator):
    def __init__(
        self,
        id: str,
        device_type: str,
        device_name: str,
        supplier: str,
        sensor: Sensor
    ):
        super().__init__(id, device_type, device_name, supplier)
        self.sensor = sensor


class SmartHouse:
    def __init__(self):
        self._devices: list[Device] = []
        self._rooms: list[Room] = []
        self._floors: list[Floor] = []

    def register_floor(self, level: int) -> Floor:
        existing_floor = self.get_floor_by_level(level)
        if existing_floor is not None:
            return existing_floor

        floor = Floor(level)
        self._floors.append(floor)
        self._floors.sort(key=lambda f: f.level)
        return floor

    def register_room(
        self,
        floor: Floor,
        room_size: float,
        room_name: Optional[str] = None
    ) -> Room:
        room = Room(floor, room_size, room_name)
        floor.add_room(room)
        self._rooms.append(room)
        return room

    def register_device(self, room: Room, device: Device) -> None:
        if device.room is not None and device.room is not room:
            device.room.remove_device(device)

        device.room = room
        room.add_device(device)

        if device not in self._devices:
            self._devices.append(device)

    def get_floors(self) -> list[Floor]:
        return list(self._floors)

    def get_floor_by_level(self, level: int) -> Optional[Floor]:
        for floor in self._floors:
            if floor.level == int(level):
                return floor
        return None

    def get_rooms(self) -> list[Room]:
        return list(self._rooms)

    def get_room_by_id(self, rid: int) -> Optional[Room]:
        for room in self._rooms:
            if room.rid == int(rid):
                return room
        return None

    def get_rooms_on_floor(self, level: int) -> list[Room]:
        floor = self.get_floor_by_level(level)
        if floor is None:
            return []
        return list(floor.rooms)

    def get_area(self) -> float:
        return round(sum(room.room_size for room in self._rooms), 2)

    def get_devices(self) -> list[Device]:
        return list(self._devices)

    def get_device_by_id(self, device_id: str) -> Optional[Device]:
        for device in self._devices:
            if device.id == str(device_id):
                return device
        return None

    def get_sensors(self) -> list[Sensor]:
        return [device for device in self._devices if device.is_sensor()]

    def get_actuators(self) -> list[Actuator]:
        return [device for device in self._devices if device.is_actuator()]