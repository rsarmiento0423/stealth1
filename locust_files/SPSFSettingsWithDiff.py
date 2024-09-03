"""SPSFSettingsWithDiff.py"""

import logging
import random
import time
from locust import events
from locust import between, task, SequentialTaskSet, HttpUser

# Configure logging
log_file_path = "locust_settings_with_diff_log1.log"

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
    deviceId_list = [
        "rohitspsf000x",
        "rohitspsf000_a",
        "rohitspsf000_b",
        "rohitspsf000_c",
        "rohitspsf000_d",
    ]
    return random.choice(deviceId_list)


def randomPause():
    """Function: randomPause"""
    return random.randint(1, 30)


class SPSFLoad(SequentialTaskSet):
    """Class: SPSFLoad"""

    @task
    def get_package_car_settings_diff(self):
        """Get Package Car Settings Diff"""
        deviceId = randomDeviceID()
        with self.client.get(
            "/pkgCarSettingsDiff?id=" + deviceId, catch_response=True
        ) as response:
            print(f"Got Package Car Settings Diff Response: {response}")
            if response.status_code != 200:
                response.failure(
                    "Failed to Package Car Get Settings Diff, StatusCode: "
                    + str(response.status_code)
                )
            elif "pkgCarId" in response.text:
                response.success()
            else:
                response.failure(
                    "Failed to Package Car Get Settings Diff, Text: " + response.text
                )
        logging.info("Wait 30 sec to run PkgCarSettingsDiff...")
        time.sleep(30)

    @task
    def get_pkgcar_settings(self):
        """Get Package Car Settings"""
        deviceId = randomDeviceID()
        with self.client.get(
            "/pkgCarSettings?id=" + deviceId, catch_response=True
        ) as response:
            print(f"Got Package Car Settings Response: {response}")
            if response.status_code != 200:
                response.failure(
                    "Failed to Package Car Get Settings, StatusCode: "
                    + str(response.status_code)
                )
            elif "ackUuid" in response.text:
                response.success()
            else:
                response.failure(
                    "Failed to Package Car Get Settings, Text: " + response.text
                )

        sleepTime = randomPause()
        logging.info("Pausing Get Package Car Settings: %s seconds", sleepTime)
        time.sleep(randomPause())

    @task
    def exit_navigation(self):
        self.interrupt()


class MyUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [SPSFLoad]
