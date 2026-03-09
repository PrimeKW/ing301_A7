from datetime import datetime
import random


class Measurement:
    def __init__(self, timestamp: str, value: float, unit: str):
        self.timestamp = str(timestamp)
        self.value = float(value)
        self.unit = str(unit)


"""Etasje og rom"""


class Floor:
    def __init__(self, level):
        self.level = int(level)
        self.rooms = []


class Room:
    def __init__(self, floor, room_size, room_name=None):
        self.floor = floor
        self.room_size = float(room_size)
        self.room_name = room_name
        self.devices = []


"""Enheter"""


class Device:
    def __init__(self, id, device_type, device_name, supplier):
        self.id = str(id)
        self.supplier = supplier
        self.model_name = device_name
        self.device_name = device_name
        self.device_type = device_type
        self.room = None

    def is_actuator(self):
        return False

    def is_sensor(self):
        return False

    def get_device_type(self):
        return str(self.device_type)


class Sensor(Device):
    def __init__(self, id, device_type, device_name, supplier, unit=None):
        super().__init__(id, device_type, device_name, supplier)
        self.unit = unit
        self._measurements = []

    def is_sensor(self):
        return True

    def add_measurement(self, value=None, unit=None):
        if unit is None:
            if self.unit is None:
                raise ValueError("Unit må oppgis første gang (eller settes på sensoren).")
            unit = self.unit
        else:
            self.unit = unit

        if value is None:
            value = random.uniform(0.0, 100.0)

        ts = datetime.now().isoformat(timespec="seconds")
        self._measurements.append(Measurement(ts, float(value), unit))

    def last_measurement(self):
        if self._measurements:
            return self._measurements[-1]

        if self.unit is None:
            raise ValueError("Sensorens unit er ikke satt.")
        ts = datetime.now().isoformat(timespec="seconds")
        return Measurement(ts, float(random.uniform(0.0, 100.0)), self.unit)

    def get_measurements(self):
        return list(self._measurements)


class Actuator(Device):
    def __init__(self, id, device_type, device_name, supplier):
        super().__init__(id, device_type, device_name, supplier)
        self._active = False
        self.target_value = None

    def is_actuator(self):
        return True

    def turn_on(self, target_value=None):
        self._active = True
        if target_value is not None:
            self.target_value = target_value

    def turn_off(self):
        self._active = False
        self.target_value = None

    def is_active(self):
        return self._active


class SmartHouse:
    def __init__(self):
        self._devices = []
        self._rooms = []
        self._floors = []

    def register_floor(self, level):
        floor = Floor(level)
        self._floors.append(floor)
        self._floors.sort(key=lambda x: x.level)
        return floor

    def register_room(self, floor, room_size, room_name=None):
        room = Room(floor, room_size, room_name)
        floor.rooms.append(room)
        self._rooms.append(room)
        return room

    def get_floors(self):
        return list(self._floors)

    def get_rooms(self):
        return list(self._rooms)

    def get_area(self):
        return round(sum(r.room_size for r in self._rooms), 2)

    def register_device(self, room, device):
        if device.room is not None and device.room is not room:
            old_room = device.room
            if device in old_room.devices:
                old_room.devices.remove(device)

        device.room = room
        if device not in room.devices:
            room.devices.append(device)

        if device not in self._devices:
            self._devices.append(device)

    def get_devices(self):
        return list(self._devices)

    def get_device_by_id(self, device_id):
        for d in self._devices:
            if d.id == device_id:
                return d
        return None