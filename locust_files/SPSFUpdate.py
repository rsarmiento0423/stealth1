"""SPSFUpdate.py"""

import json
import logging
from locust import events
from locust import between, task, SequentialTaskSet, HttpUser

# Configure logging
log_file_path = "locust_update_settings_log.log"

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


class SPSFLoad(SequentialTaskSet):
    @task
    def update_settings(self):
        """Update Settings"""
        json_file_path = "data/update.json"

        with open(json_file_path, "r", encoding="ascii") as j:
            contents = json.loads(j.read())
        payload = contents
        hdrs = {"Content-type": "application/json"}

        with self.client.put(
            "/gwSettings", data=json.dumps(payload), headers=hdrs, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(
                    "Failed to Update Settings, StatusCode: "
                    + str(response.status_code)
                )
            else:
                if "carType" in response.text:
                    response.success()
                else:
                    response.failure(
                        "Failed to Update Settings, Text: " + response.text
                    )

    @task
    def exit_navigation(self):
        self.interrupt()


class MyUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [SPSFLoad]
