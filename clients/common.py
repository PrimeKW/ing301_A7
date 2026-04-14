import json

# base URL for the cloud service - can be used to avoid dependency on deployment
BASE_URL = "http://localhost:8000/smarthouse/"

TEMPERATURE_SENSOR_DID = "4d8b1d62-7921-4917-9b70-bbd31f6e2e8e"
LIGHT_BULB_ACTUATOR_DID = '6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28'

class SensorMeasurement:
    """
    Class representing measurements exchanged between temperature sensor client
    and cloud service in Json format
    """

    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit

    def to_json_str(self):

        sensor_measurement_json_str = json.dumps(self.__dict__)

        return sensor_measurement_json_str

    @staticmethod
    def from_json_str(measurement_json_str: str):

        measurement_dict = json.loads(measurement_json_str)

        measurement = SensorMeasurement(measurement_dict['timestamp'],
                                        measurement_dict['value'],
                                        measurement_dict['unit'])

        return measurement

class ActuatorState:
    """
    Class representing actuator state exchanged between temperature
    sensor client and cloud service in Json format
    """

    def __init__(self, state):
        self.state = state

    def set_state(self, new_state):
        self.state = new_state

    def to_json_str(self):
        state_json_str = json.dumps(self.__dict__)

        return state_json_str

    @staticmethod
    def from_json_str(state_json_str: str):

        state_dict = json.loads(state_json_str)
        state = ActuatorState(state_dict['state'])

        return state