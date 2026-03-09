from smarthouse.domain import SmartHouse, Sensor, Actuator

DEMO_HOUSE = SmartHouse()

# Building house structure
first_floor = DEMO_HOUSE.register_floor(1)
second_floor = DEMO_HOUSE.register_floor(2)

# Første etasje
Entrance = DEMO_HOUSE.register_room(first_floor, 13.5, "Entrance")
Living_room = DEMO_HOUSE.register_room(first_floor, 39.75, "Living Room")
Bathroom1 = DEMO_HOUSE.register_room(first_floor, 6.3, "Bathroom 1")
Garage = DEMO_HOUSE.register_room(first_floor, 19, "Garage")
Guest_room1 = DEMO_HOUSE.register_room(first_floor, 8, "Guest Room 1")

# Andre Etasje
Office = DEMO_HOUSE.register_room(second_floor, 11.75, "Office")
Bathroom2 = DEMO_HOUSE.register_room(second_floor, 9.25, "Bathroom 2")
Guest_room2 = DEMO_HOUSE.register_room(second_floor, 8, "Guest Room 2")
Hallway = DEMO_HOUSE.register_room(second_floor, 10, "Hallway")
Guest_room3 = DEMO_HOUSE.register_room(second_floor, 10, "Guest Room 3")
Dressing_room = DEMO_HOUSE.register_room(second_floor, 4, "Dressing room")
Master_bedroom = DEMO_HOUSE.register_room(second_floor, 17, "Master bedroom")

# Enheter
smart_lock = Actuator(
    "4d5f1ac6-906a-4fd1-b4bf-3a0671e4c4f1",
    "Smart Lock",
    "Guardian Lock 7000",
    "MythicalTech"
)
DEMO_HOUSE.register_device(Entrance, smart_lock)

co2_sensor = Sensor(
    "8a43b2d7-e8d3-4f3d-b832-7dbf37bf629e",
    "CO2 sensor",
    "Smoke Warden 1000",
    "ElysianTech"
)
DEMO_HOUSE.register_device(Living_room, co2_sensor)

electricity_meter = Actuator(
    "a2f8690f-2b3a-43cd-90b8-9deea98b42a7",
    "Electricity meter",
    "Volt Watch Elite",
    "MysticEnergy Innovations"
)
DEMO_HOUSE.register_device(Entrance, electricity_meter)

heat_pump = Actuator(
    "5e13cabc-5c58-4bb3-82a2-3039e4480a6d",
    "Heat Pump",
    "Thermo Smart 6000",
    "ElysianTech"
)
DEMO_HOUSE.register_device(Living_room, heat_pump)

motion_sensor = Sensor(
    "cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5",
    "Motion Sensor",
    "MoveZ Detect 69",
    "NebulaGuard Innovations"
)
DEMO_HOUSE.register_device(Living_room, motion_sensor)

humidity_sensor = Sensor(
    "3d87e5c0-8716-4b0b-9c67-087eaaed7b45",
    "Humidity sensor",
    "Aqua Alert 800",
    "AetherCorp"
)
DEMO_HOUSE.register_device(Bathroom1, humidity_sensor)

smart_oven = Actuator(
    "8d4e4c98-21a9-4d1e-bf18-523285ad90f6",
    "Smart Oven",
    "Pheonix HEAT 333",
    "AetherCorp"
)
DEMO_HOUSE.register_device(Guest_room1, smart_oven)

automatic_garage_door = Actuator(
    "9a54c1ec-0cb5-45a7-b20d-2a7349f1b132",
    "Automatic Garage Door",
    "Guardian Lock 9000",
    "MythicalTech"
)
DEMO_HOUSE.register_device(Garage, automatic_garage_door)

smart_oven1 = Actuator(
    "c1e8fa9c-4b8d-487a-a1a5-2b148ee9d2d1",
    "Smart Oven",
    "Ember Heat 3000",
    "IgnisTech Solutions"
)
DEMO_HOUSE.register_device(Master_bedroom, smart_oven1)

temperature_sensor = Sensor(
    "4d8b1d62-7921-4917-9b70-bbd31f6e2e8e",
    "Temperature sensor",
    "SmartTemp 42",
    "AetherCorp"
)
DEMO_HOUSE.register_device(Master_bedroom, temperature_sensor)

air_quality_sensor = Sensor(
    "7c6e35e1-2d8b-4d81-a586-5d01a03bb02c",
    "Air Quality sensor",
    "AeroGuard Pro",
    "CelestialSense Technologies"
)
DEMO_HOUSE.register_device(Guest_room3, air_quality_sensor)

smart_plug = Actuator(
    "1a66c3d6-22b2-446e-bf5c-eb5b9d1a8c79",
    "Smart Plug",
    "FlowState X",
    "MysticEnergy Innovations"
)
DEMO_HOUSE.register_device(Office, smart_plug)

dehumidifier = Actuator(
    "9e5b8274-4e77-4e4e-80d2-b40d648ea02a",
    "Dehumidifier",
    "Hydra Dry 8000",
    "ArcaneTech Solutions"
)
DEMO_HOUSE.register_device(Bathroom2, dehumidifier)

light_bulp = Actuator(
    "6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28",
    "Light Bulp",
    "Lumina Glow 4000",
    "Elysian Tech"
)
DEMO_HOUSE.register_device(Guest_room2, light_bulp)

temperature_sensor.add_measurement(21.0, "°C")