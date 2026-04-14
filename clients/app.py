import common
import requests


class SmartHouseApp:
    """
    Class representing an end-user client application that can
    interact with the device clients via the cloud service.

    The application is highly simplistic being only capable of
    controlling a temperature sensor and a light bulb actuator
    """

    def __init__(self):
        self.sensor_did = common.TEMPERATURE_SENSOR_DID
        self.actuator_did = common.LIGHT_BULB_ACTUATOR_DID

    def get_bulb_state(self):
        """
        This method sends a GET request to the cloud state to obtain
        the current state of the light bulb actuator
        """

        url = common.BASE_URL + f"actuator/{self.actuator_did}/state"

        try:
            response = requests.get(url, timeout=5)

            if response.status_code != 200:
                print(f"Failed to get bulb state. Status code: {response.status_code}")
                return None

            actuator_state = common.ActuatorState.from_json_str(response.text)
            return actuator_state.state

        except requests.RequestException as e:
            print(f"Error while getting bulb state: {e}")
            return None

    def update_bulb_state(self, new_state) -> requests.Response:
        """
        This method sends a PUT request to the cloud state to update
        the current state of the light bulb actuator
        """

        url = common.BASE_URL + f"actuator/{self.actuator_did}/state"

        if new_state == "on":
            payload = {"state": True}
        else:
            payload = {"state": False}

        try:
            response = requests.put(url, json=payload, timeout=5)
            return response
        except requests.RequestException as e:
            print(f"Error while updating bulb state: {e}")
            return None

    def get_temperature(self):
        """
        This method sends a GET request to the cloud state to obtain
        the current temperature recorded for the temperature sensor
        """

        url = common.BASE_URL + f"sensor/{self.sensor_did}/current"

        try:
            response = requests.get(url, timeout=5)

            if response.status_code != 200:
                print(f"Failed to get temperature. Status code: {response.status_code}")
                return None

            measurement = common.SensorMeasurement.from_json_str(response.text)
            return measurement.value

        except requests.RequestException as e:
            print(f"Error while getting temperature: {e}")
            return None

    def main(self):

        is_active = True

        while is_active:

            print("---- SmartHouse Control App ----")
            print("Select option:")
            print("1. Toggle Lightbulb")
            print("2. Show Temperature")
            print("3. Quit")

            user_input = input(">>> ")

            if not user_input.isdigit() or int(user_input) not in {1, 2, 3}:
                print(f"Unrecognized input: '{user_input}'")
                continue

            selected_option = int(user_input)

            if selected_option == 1:

                current_state = self.get_bulb_state()

                if current_state is None:
                    print("Could not read current bulb state.")
                    continue

                print(f"Current state lightbulb: {current_state}")

                if current_state == "off" or current_state is False:
                    current_state = "on"
                else:
                    current_state = "off"

                response = self.update_bulb_state(current_state)

                if response is not None:
                    print(f"Update bulb response status: {response.status_code}")

                new_state = self.get_bulb_state()
                print(f"New state lightbulb: {new_state}")

            elif selected_option == 2:

                value = self.get_temperature()

                if value is not None:
                    print(f"Current temperature: {value}")

            else:
                is_active = False

        print("App shutting down")


if __name__ == '__main__':
    app = SmartHouseApp()
    app.main()