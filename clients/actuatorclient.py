"""
    Bruker API (spør om API tilstand, oppdaterer egen, logger, gjentar)
    """

import time
import requests
import logging

log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")

import common

LIGHTBULB_CLIENT_SLEEP_TIME = 4


class ActuatorClient:

    def __init__(self, did):
        self.did = did
        self.state = common.ActuatorState("off")

    def get_state(self) -> str:

        logging.info(f"Actuator Client {self.did} retrieving state")

        url = f"{common.BASE_URL}/smarthouse/actuator/{self.did}/state"

        try:
            response = requests.get(url, timeout=5)
            logging.info(f"GET {url} -> {response.status_code}")

            if response.status_code != 200:
                logging.warning(f"Could not retrieve actuator state for {self.did}")
                return self.state.state

            data = response.json()

            if data.get("state") is True:
                actuator_state = "on"
            else:
                actuator_state = "off"

            return actuator_state

        except requests.RequestException as e:
            logging.error(f"Failed to retrieve state for {self.did}: {e}")
            return self.state.state

    def run(self):

        while True:
            new_state = self.get_state()

            if new_state != self.state.state:
                self.state = common.ActuatorState(new_state)
                logging.info(f"Actuator {self.did} set to {self.state.state}")
            else:
                logging.info(f"Actuator {self.did} remains {self.state.state}")

            time.sleep(LIGHTBULB_CLIENT_SLEEP_TIME)


if __name__ == '__main__':
    actuator = ActuatorClient(common.LIGHT_BULB_ACTUATOR_DID)
    actuator.run()