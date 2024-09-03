"""SPSFApplyInternalSettingsFacilityExternalCarType.py"""

import json
import logging
from locust import events
from locust import between, task, HttpUser

# Configure logging
log_file_path = "locust_apply_internal_settings_facility_external_cartype_log.log"

# Set up the logging to append to a file
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, mode="a"),  # Append mode
        logging.StreamHandler(),  # Also log to console (optional)
    ],
)


# Event listener to stop the test after the desired number of requests
@events.quitting.add_listener
def _quiting(environment, **kw):
    logging.debug("Quitting event triggered")
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


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logging.info(
        "..........SPSF Apply Internal Settings With Facility and External CarType Load Test started.........."
    )


# Example event listener to log when Locust stops
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    environment.runner.quit()
    logging.info(
        "..........SPSF Apply Internal Settings With Facility and External CarType Load Test stopped.........."
    )


class SPSFLoad(HttpUser):
    """Class: SPSFLoad"""

    wait_time = between(1, 2)

    @task
    def end_to_end_internal(self):
        ### Apply Internal Settings
        logging.info("Apply Internal Settings API...")
        try:
            json_file_path = "data/facility_external_cartype_all_patches.json"
            with open(json_file_path, "r", encoding="ascii") as j:
                contents = json.loads(j.read())
            payload = contents
            headers = {"Content-Type": "application/json"}
            with self.client.patch(
                "/api/v1/applySettings",
                json=payload,
                headers=headers,
                catch_response=True,
            ) as response:
                logging.info("Apply Internal Settings Response: %s", response)
                if response.status_code != 204:
                    logging.error("Unexpected status code: %d", response.status_code)
                    response.failure(
                        f"Failure to execute Apply Internal Settings API due to Status Code: {response.status_code}"
                    )
                    raise AssertionError("Expecting 204 status code!")
        except AssertionError as e:
            logging.error("An error occurred: %s", e)
