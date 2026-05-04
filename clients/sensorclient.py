"""
    Sender til API (Måler en temp, sender, gjenta)
    """

import time
import math
import requests
import datetime
import logging

import common

log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")

TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME = 4
TEMP_RANGE = 40


class SensorClient:
    """
    Sensor client representing the physical temperature sensor
    in the house and reporting temperature to the cloud service.
    """

    def __init__(self, did):
        self.did = did

    def do_measurement(self) -> common.SensorMeasurement:
        """
        Method simulating the reading of a temperature on the sensor.
        """
        logging.info(f"Sensor {self.did} measuring")

        temp = round(math.sin(time.time() / 10) * TEMP_RANGE, 1)

        logging.info(f"Sensor measured {self.did}: {temp}")

        return common.SensorMeasurement(
            datetime.datetime.now().isoformat(),
            temp,
            "°C"
        )

    def put_measurement(self, m: common.SensorMeasurement) -> requests.Response:
        """
        Sends a PUT request to update the current temperature
        recorded in the cloud service.
        """
        logging.info(f"Sensor client {self.did} update starting")

        url = f"{common.BASE_URL}/smarthouse/sensor/{self.did}/current"

        payload = {
            "timestamp": m.timestamp,
            "value": float(m.value),
            "unit": m.unit
        }

        response = requests.put(url, json=payload, timeout=5)

        logging.info(f"PUT {url} -> {response.status_code}")

        if response.status_code >= 400:
            logging.error(f"Response body: {response.text}")

        return response

    def run(self):
        """
        Runs in a loop, regularly reading the temperature
        and sending it to the cloud service.
        """
        while True:
            measurement = self.do_measurement()
            self.put_measurement(measurement)
            time.sleep(TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME)


if __name__ == "__main__":
    sensor = SensorClient(common.TEMPERATURE_SENSOR_DID)
    sensor.run()