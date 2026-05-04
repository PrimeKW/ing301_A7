"""Kobling mellom SQL/databasen og Python objekter"""

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

        # Rooms + Floors
        rooms_by_id = {}
        floors_by_level = {}

        c.execute("SELECT id, floor, area, name FROM rooms")
        for room_id, floor_level, room_size, room_name in c.fetchall():
            if floor_level not in floors_by_level:
                floor = Floor(floor_level)
                floors_by_level[floor_level] = floor
                house._floors.append(floor)
            else:
                floor = floors_by_level[floor_level]

            room = Room(floor, room_size, room_name)
            room.id = room_id
            rooms_by_id[room_id] = room
            floor.rooms.append(room)
            house._rooms.append(room)

        # Devices
        c.execute("SELECT id, room, kind, category, supplier, product FROM devices")
        for device_id, room_id, kind, category, supplier, product in c.fetchall():
            room = rooms_by_id[room_id]

            if category.lower() == "sensor":
                device = Sensor(device_id, kind, product, supplier)
            else:
                device = Actuator(device_id, kind, product, supplier)

            device.room = room
            room.devices.append(device)
            house._devices.append(device)

        # Measurements
        c.execute("SELECT device, ts, value, unit FROM measurements")
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
            SELECT ts, value, unit
            FROM measurements
            WHERE device = ?
            ORDER BY ts DESC
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

    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None,
                                      until_date: Optional[str] = None) -> dict:
        c = self.conn.cursor()

        query = """
                SELECT substr(m.ts, 1, 10) AS day,
                   ROUND(AVG(m.value), 4) AS avg_temp
                FROM measurements m
                    JOIN devices d \
                ON m.device = d.id
                WHERE d.room = ?
                  AND m.unit = '°C' \
                """
        params = [room.id]

        if from_date is not None:
            query += " AND substr(m.ts, 1, 10) >= ?"
            params.append(from_date)

        if until_date is not None:
            query += " AND substr(m.ts, 1, 10) <= ?"
            params.append(until_date)

        query += """
            GROUP BY substr(m.ts, 1, 10)
            ORDER BY day
        """

        c.execute(query, params)
        rows = c.fetchall()
        c.close()

        return {day: avg_temp for day, avg_temp in rows}

    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        c = self.conn.cursor()

        query = """
                WITH room_humidity AS 
                            (SELECT m.ts, m.value \
                            FROM measurements m \
                            JOIN devices d ON m.device = d.id \
                            WHERE d.room = ? \
                            AND lower(d.kind) LIKE '%humidity%' \
                            AND substr(m.ts, 1, 10) = ?),
                     avg_humidity AS (SELECT AVG(value) AS avg_val \
                            FROM room_humidity)
                SELECT CAST(substr(rh.ts, 12, 2) AS INTEGER) AS hour
                FROM room_humidity rh, avg_humidity ah
                WHERE rh.value > ah.avg_val
                GROUP BY hour
                HAVING COUNT (*) > 3
                ORDER BY hour \
                """

        c.execute(query, (room.id, date))
        rows = c.fetchall()
        c.close()

        return [hour for (hour,) in rows]