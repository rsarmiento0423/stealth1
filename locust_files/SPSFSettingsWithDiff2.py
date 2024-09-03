"""SPSFSettingsWithDiff2.py"""

import json
import logging
import random
import time
from locust import events
from locust import between, task, SequentialTaskSet, HttpUser

# Configure logging
log_file_path = "locust_settings_with_diff_log.log"

# Set up the logging to append to a file
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, mode="a"),  # Append mode
        logging.StreamHandler(),  # Also log to console (optional)
    ],
)


@events.quitting.add_listener
def _quiting(environment, **kw):
    if environment.stats.total.fail_ratio > 0.01:
        logging.error("Test failed due to failure ratio > 1%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 200:
        logging.error("Test failed due to average response time ratio > 200 ms")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 800:
        logging.error("Test failed due to 95th percentile response time > 800 ms")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0


def randomDeviceID():
    """Function: randomDeviceID"""
    deviceId_list = ["001f7b3f2094", "001f7b3f1d3c"]
    return random.choice(deviceId_list)


def randomPause():
    """Function: randomPause"""
    return random.randint(300, 900)


class SPSFLoad(SequentialTaskSet):
    """Class: SPSFLoad"""

    @task
    def get_pkgcar_settings(self):
        """Get Package Car Settings API"""
        deviceId = randomDeviceID()
        with self.client.get(
            "/pkgCarSettings?id=" + deviceId, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(
                    "Failed to execute Get Package Car Settings API due to Status Code: "
                    + str(response.status_code)
                )
            elif "ackUuid" in response.text:
                response.success()
            else:
                response.failure("Expected response from Get Package Car Settings API!")

        sleepTime = randomPause()
        logging.info(
            "Wait randomly at: %d seconds before executing the next Get Package Car Settings API...",
            sleepTime,
        )
        time.sleep(randomPause())

    @task
    def get_package_car_settings_combo(self):
        """Get Package Car Settings API Combo"""
        ### Get Package Settings Diff
        deviceId = randomDeviceID()
        logging.info("Get Get Package Car Settings Diff API for deviceID: %s", deviceId)
        with self.client.get(
            "/pkgCarSettingsDiff?id=" + deviceId, catch_response=True
        ) as response:
            logging.info("Got Get Package Car Settings Diff Response: %s", response)
            if response.status_code != 200:
                response.failure(
                    "Failed to execute Get Package Car Settings Diff API due to Status Code: "
                    + str(response.status_code)
                )
            elif "pkgCarId" in response.text:
                response_data = json.loads(response.text)
                ACTUAL_ackUuID = response_data[0]["ackUuid"]
                logging.info("Got Actual ackUuid: %s", ACTUAL_ackUuID)
                response.success()
            else:
                response.failure(
                    "Expected response from Get Package Settings Diff API!"
                )

        ### Get Package Car Ack
        logging.info("Get Package Car Ack API for deviceID: %s", deviceId)
        headers = {"Content-Type": "application/json"}
        payload = {"ackUuid": ACTUAL_ackUuID}
        with self.client.post(
            "/pkgCarSettingsAck", json=payload, headers=headers, catch_response=True
        ) as response:
            logging.info("Response: %s", response)
            if response.status_code != 200:
                response.failure(
                    "Failure to execute Get Package Car Ack API due to Status Code: "
                    + str(response.status_code)
                )

        logging.info("Wait 30 sec to execute the next PkgCarSettingsDiff API...")
        time.sleep(30)

    @task
    def exit_navigation(self):
        self.interrupt()


class MyUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [SPSFLoad]
