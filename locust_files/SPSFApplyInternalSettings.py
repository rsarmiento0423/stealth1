"""SPSFApplyInternalSettings.py"""

import json
import logging
from locust import events
from locust import between, task, HttpUser

# Configure logging
log_file_path = "locust_apply_internal_settings_log.log"

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
    logging.info("..........SPSF Apply Internal Settings Load Test started..........")


# Example event listener to log when Locust stops
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    environment.runner.quit()
    logging.info("..........SPSF Apply Internal Settings Load Test stopped..........")


class SPSFLoad(HttpUser):
    """Class: SPSFLoad"""

    wait_time = between(1, 2)
    # stop_test_time = time.time() + 120
    total_requests = 110  # Total number of requests to execute
    request_counter = 0

    mac_ids = [
        "001f7b3efe62",
        "001f7b3f1abc",
        "001f7b3f1cdc",
        "001f7b3f1d00",
        "001f7b3f1d0c",
        "001f7b3f1d1e",
        "001f7b3f1d22",
        "001f7b3f1d3a",
        "001f7b3f1d3c",
        "001f7b3f1d48",
        "001f7b3f1d5a",
        "001f7b3f1d5c",
        "001f7b3f1db4",
        "001f7b3f1dc2",
        "001f7b3f1df0",
        "001f7b3f1e14",
        "001f7b3f1e8e",
        "001f7b3f1eb2",
        "001f7b3f1ed6",
        "001f7b3f1f58",
        "001f7b3f1f7a",
        "001f7b3f1fde",
        "001f7b3f2044",
        "001f7b3f2094",
        "001f7b3f2096",
        "001f7b3f2098",
        "001f7b3f209a",
        "001f7b3fc5dc",
        "001f7b3fc5e0",
        "001f7b3fc5e2",
        "001f7b3fc5e6",
        "001f7b3fc5e8",
        "001f7b3fc5ec",
        "001f7b3fc5fe",
        "001f7b3fc600",
        "001f7b3fc602",
        "001f7b3fc608",
        "001f7b3fc60a",
        "001f7b3fc610",
        "001f7b3fc614",
        "001f7b3fc61a",
        "001f7b3fc61e",
        "001f7b3fc624",
        "001f7b3fc62a",
        "001f7b3fc62c",
        "001f7b3fc630",
        "001f7b3fc632",
        "001f7b3fc634",
        "001f7b3fc63c",
        "001f7b3fc63e",
        "001f7b3fc656",
        "001f7b3fc658",
        "001f7b3fc65c",
        "001f7b3fc65e",
        "001f7b3fc662",
        "001f7b3fc664",
        "001f7b3fc668",
        "001f7b3fc66e",
        "001f7b3fc670",
        "001f7b3fc672",
        "001f7b3fc674",
        "001f7b3fc676",
        "001f7b3fc67a",
        "001f7b3fc680",
        "001f7b3fc68e",
        "001f7b3fc690",
        "001f7b3fc694",
        "001f7b3fc6be",
        "001f7b3fc6c0",
        "001f7b3fc6c2",
        "001f7b3fc6e6",
        "001f7b3fc6ea",
        "001f7b3fc6ec",
        "001f7b3fc6f6",
        "001f7b3fc6f8",
        "001f7b3fc702",
        "001f7b3fc706",
        "001f7b3fc708",
        "001f7b3fc70a",
        "001f7b3fc720",
        "001f7b3fc726",
        "001f7b3fc72a",
        "001f7b3fc72c",
        "001f7b3fc740",
        "001f7b3fc74a",
        "001f7b3fc758",
        "001f7b3fc75a",
        "001f7b3fc75c",
        "001f7b3fc762",
        "001f7b3fc764",
        "001f7b3fc768",
        "001f7b3fc76e",
        "001f7b3fc776",
        "001f7b3fc778",
        "001f7b3fc77c",
        "001f7b3fc77e",
        "001f7b3fc780",
        "001f7b3fc784",
        "001f7b3fc786",
        "001f7b3fc788",
        "001f7b3fc78a",
        "001f7b3fc79e",
        "001f7b3fc7a0",
        "001f7b3fc7d8",
        "001f7b3fc7da",
        "001f7b3fc7e2",
        "001f7b3fc7e8",
        "001f7b3fc7fe",
        "001f7b3fc802",
        "001f7b3fc806",
    ]

    @task
    def end_to_end_internal(self):
        ### Apply Internal Settings
        logging.info("Apply Internal Settings API...")
        for macid in self.mac_ids:
            logging.info("Request counter: %d,", self.request_counter)
            if self.request_counter >= self.total_requests:
                logging.info(
                    "Stop the Locust instance once the desired number of requests %d is reached",
                    self.request_counter,
                )
                self.environment.runner.quit()
            try:
                json_file_path = "data/all_internal_settings_single.json"
                with open(json_file_path, "r", encoding="ascii") as j:
                    contents = json.loads(j.read())
                payload = contents
                payload["tapeIds"] = [macid]
                logging.info("Got tapeID: %s", macid)
                headers = {"Content-Type": "application/json"}
                with self.client.patch(
                    "/api/v1/applySettings",
                    json=payload,
                    headers=headers,
                    catch_response=True,
                ) as response:
                    logging.info("Apply Internal Settings Response: %s", response)
                    if response.status_code != 204:
                        logging.error(
                            "Unexpected status code: %d", response.status_code
                        )
                        response.failure(
                            f"Failure to execute Apply Internal Settings API due to Status Code: {response.status_code}"
                        )
                        raise AssertionError("Expecting 204 status code!")
                self.request_counter += 1
                logging.info("Request executed: %d", self.request_counter)
            except AssertionError as e:
                logging.error("An error occurred: %s", e)
