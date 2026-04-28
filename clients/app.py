import common
import requests


class SmartHouseApp:
    def __init__(self):
        self.sensor_did = common.TEMPERATURE_SENSOR_DID
        self.actuator_did = common.LIGHT_BULB_ACTUATOR_DID

    def get_bulb_state(self):
        url = f"{common.BASE_URL}/smarthouse/actuator/{self.actuator_did}/state"

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

    def update_bulb_state(self, new_state) -> requests.Response | None:
        url = f"{common.BASE_URL}/smarthouse/actuator/{self.actuator_did}/state"

        payload = {
            "state": new_state == "on"
        }

        try:
            return requests.put(url, json=payload, timeout=5)
        except requests.RequestException as e:
            print(f"Error while updating bulb state: {e}")
            return None

    def get_temperature(self):
        url = f"{common.BASE_URL}/smarthouse/sensor/{self.sensor_did}/current"

        try:
            response = requests.get(url, timeout=5)

            if response.status_code != 200:
                print(f"Failed to get temperature. Status code: {response.status_code}")
                return None

            measurement = common.SensorMeasurement.from_json_str(response.text)
            return f"{measurement.value} {measurement.unit}"

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

                if current_state is False:
                    new_state = "on"
                else:
                    new_state = "off"

                response = self.update_bulb_state(new_state)

                if response is not None:
                    print(f"Update bulb response status: {response.status_code}")

                updated_state = self.get_bulb_state()
                print(f"New state lightbulb: {updated_state}")

            elif selected_option == 2:
                value = self.get_temperature()

                if value is not None:
                    print(f"Current temperature: {value}")

            else:
                is_active = False

        print("App shutting down")


if __name__ == "__main__":
    app = SmartHouseApp()
    app.main()