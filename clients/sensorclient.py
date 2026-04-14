import time
import math
import requests
import datetime
import logging

log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")

import common

TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME = 4
TEMP_RANGE = 40

class SensorClient:
    """
    Sensor client representing the physical temperature sensor
    in the house and reporting temperature to the cloud service
    """

    def __init__(self, did):
        self.did = did

    def do_measurement(self) -> common.SensorMeasurement:
        """
        Method simulating the reading of a temperature on the sensor
        """
        logging.info(f"Sensor {self.did} measuring")

        temp = round(math.sin(time.time() / 10) * TEMP_RANGE, 1)

        logging.info(f"Sensor measured {self.did}: {temp}")

        measurement =  common.SensorMeasurement(str(datetime.datetime.now().isoformat()),
                                                str(temp),"Deg C")

        return measurement

    def put_measurement(self,m: common.SensorMeasurement) -> requests.Response:
        """
        This method sends a PUT request to update the current temperature
        recorded in the cloud service
        """

        logging.info(f"Sensor client {self.did} update starting")
        response = None

        # TODO
        return response


    def run(self):
        """
        This method runs in a loop reguarly reading the temperature
        and sending it to the cloud service
        """

        while True:

            m = self.do_measurement()

            r = self.put_measurement(m)

            time.sleep(TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME)

if __name__ == '__main__':

    sensor = SensorClient(common.TEMPERATURE_SENSOR_DID)
    sensor.run()