"""
    Oversetter Client (Bestemmer hvordan man oversetter mellom JSON og Python objekter)
    Denne bruker Clientene
    """

import json

BASE_URL = "http://localhost:8000"  #IP som requests sendes til

TEMPERATURE_SENSOR_DID = "4d8b1d62-7921-4917-9b70-bbd31f6e2e8e" # Sensoren som gjør målinger
LIGHT_BULB_ACTUATOR_DID = "6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28" #  Actuator som endres


class SensorMeasurement:
    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit

    def to_json_str(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json_str(measurement_json_str: str):
        measurement_dict = json.loads(measurement_json_str)
        return SensorMeasurement(
            measurement_dict["timestamp"],
            measurement_dict["value"],
            measurement_dict["unit"]
        )


class ActuatorState:
    def __init__(self, state):
        self.state = state

    def to_json_str(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json_str(state_json_str: str):
        state_dict = json.loads(state_json_str)
        return ActuatorState(state_dict["state"])