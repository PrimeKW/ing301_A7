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

    def get_bulb_state(self) -> str:
        """
        This method sends a GET request to the cloud state to obtain
        the current state of the light bulb actuator
        """

        url = common.BASE_URL + f"actuator/{self.actuator_did}/state"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        actuator_state = common.ActuatorState.from_json_str(response.text)

        return actuator_state.state

    def update_bulb_state(self,new_state) -> requests.Response:
        """
        This method sends a PUT request to the cloud state to obtain
        the current state of the light bulb actuator
        """

        # TODO START

        pass

        # TODO END

    def get_temperature(self) -> float:
        """
        This method sends a GET request to the cloud state to obtain
        the current temperature recorded for the temperature sensor
        """

        # TODO START

        pass

        # TODO END

    def main(self):

        is_active = True

        while is_active:

            print("---- SmartHouse Control App ----\nSelect option:\n1. Toggle Lightbulb \n2. Show Temperature\n3. Quit\n")
            user_input = input(">>> ")

            if not user_input.isdigit() and int(user_input) in {1, 2, 3}:
                print(f"Unrecognized input: '{user_input}'")
            else:
                selected_option = int(user_input)
                if selected_option == 1:

                    current_state = self.get_bulb_state()
                    print(f'Current state lightbulb: {current_state}')

                    if current_state == 'off':
                        current_state = 'on'
                    else:
                        current_state = 'off'

                    self.update_bulb_state(current_state)
                    new_state = self.get_bulb_state()
                    print(f'New state lightbulb: {new_state}')

                elif selected_option == 2:

                    value = self.get_temperature()
                    print(f'Current temperature: {value}')

                else:
                    is_active = False

        print("App shutting down")

if __name__ == '__main__':
    app = SmartHouseApp()
    app.main()
