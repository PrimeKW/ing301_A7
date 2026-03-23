import sqlite3
from typing import Optional
from smarthouse.domain import Measurement, SmartHouse, Floor, Room, Sensor, Actuator


class SmartHouseRepository:
    def __init__(self, file: str) -> None:
        self.file = file
        self.conn = sqlite3.connect(file, check_same_thread=False)

    def __del__(self):
        self.conn.close()

    def cursor(self) -> sqlite3.Cursor:
        return self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)

    def load_smarthouse_deep(self):
        c = self.conn.cursor()
        house = SmartHouse()

        # Floors
        floors_by_id = {}
        c.execute("SELECT id, level FROM floors")
        for floor_id, level in c.fetchall():
            floor = Floor(level)
            floors_by_id[floor_id] = floor
            house._floors.append(floor)

        # Rooms
        rooms_by_id = {}
        c.execute("SELECT id, floor_id, room_size, room_name FROM rooms")
        for room_id, floor_id, room_size, room_name in c.fetchall():
            floor = floors_by_id[floor_id]
            room = Room(floor, room_size, room_name)
            rooms_by_id[room_id] = room
            floor.rooms.append(room)
            house._rooms.append(room)

        # Devices
        c.execute("SELECT id, room_id, device_type, model_name, supplier FROM devices")
        for device_id, room_id, device_type, model_name, supplier in c.fetchall():
            room = rooms_by_id[room_id]
            dt = device_type.lower()

            if "sensor" in dt or dt in ["temperature", "humidity", "motion"]:
                device = Sensor(device_id, device_type, model_name, supplier)
            else:
                device = Actuator(device_id, device_type, model_name, supplier)

            device.room = room
            room.devices.append(device)
            house._devices.append(device)

        # Measurements
        c.execute("SELECT device_id, timestamp, value, unit FROM measurements")
        for device_id, timestamp, value, unit in c.fetchall():
            device = house.get_device_by_id(device_id)
            if isinstance(device, Sensor):
                device._measurements.append(Measurement(timestamp, value, unit))

        # Actuator states
        c.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name='actuator_states'
        """)
        if c.fetchone():
            c.execute("SELECT device_id, is_active, target_value FROM actuator_states")
            for device_id, is_active, target_value in c.fetchall():
                device = house.get_device_by_id(device_id)

                if isinstance(device, Actuator):
                    if is_active:
                        device.turn_on(target_value)
                    else:
                        device.turn_off()

        c.close()
        return house

    def get_latest_reading(self, sensor) -> Optional[Measurement]:

        if sensor is None or not sensor.is_sensor():
            return None

        c = self.conn.cursor()
        c.execute("""
            SELECT timestamp, value, unit
            FROM measurements
            WHERE device_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (sensor.id,))

        row = c.fetchone()
        c.close()

        if row is None:
            return None

        timestamp, value, unit = row
        return Measurement(timestamp, value, unit)

    def update_actuator_state(self, actuator):

        if actuator is None or not actuator.is_actuator():
            return

        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS actuator_states (
                device_id TEXT PRIMARY KEY,
                is_active INTEGER NOT NULL,
                target_value REAL
            )
        """)

        is_active = 1 if actuator.is_active() else 0
        target_value = actuator.target_value

        c.execute("""
            INSERT INTO actuator_states (device_id, is_active, target_value)
            VALUES (?, ?, ?)
            ON CONFLICT(device_id) DO UPDATE SET
                is_active = excluded.is_active,
                target_value = excluded.target_value
        """, (actuator.id, is_active, target_value))

        self.conn.commit()
        c.close()

    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> dict:
        return NotImplemented

    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        return NotImplemented