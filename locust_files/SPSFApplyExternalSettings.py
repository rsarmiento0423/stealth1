"""SPSFApplyExternalSettings.py"""

import json
import logging
from locust import events
from locust import between, task, HttpUser

# Configure logging
log_file_path = "locust_apply_external_settings_log.log"

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
    logging.info("..........SPSF Apply External Settings Load Test started..........")


# Example event listener to log when Locust stops
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    environment.runner.quit()
    logging.info("..........SPSF Apply External Settings Load Test stopped..........")


class SPSFLoad(HttpUser):
    """Class: SPSFLoad"""

    wait_time = between(1, 2)
    # stop_test_time = time.time() + 120
    total_requests = 110  # Total number of requests to execute
    request_counter = 0

    device_ids = [
        "UPSP128130",
        "UPSP128152",
        "UPSP128156",
        "UPSP128176",
        "UPSP128249",
        "UPSP128251",
        "UPSP128268",
        "UPSP128282",
        "UPSP128283",
        "UPSP146944",
        "UPSP146998",
        "UPSP148724",
        "UPSP148833",
        "UPSP148834",
        "UPSP148837",
        "UPSP148838",
        "UPSP149657",
        "UPSP149660",
        "UPSP149661",
        "UPSP149662",
        "UPSP151656",
        "UPSP151673",
        "UPSP151678",
        "UPSP151770",
        "UPSP151852",
        "UPSP155495",
        "UPSP155504",
        "UPSP155686",
        "UPSP157353",
        "UPSP157358",
        "UPSP157515",
        "UPSP157529",
        "UPSP157890",
        "UPSP159279",
        "UPSP159531",
        "UPSP163758",
        "UPSP163759",
        "UPSP163798",
        "UPSP168383",
        "UPSP168585",
        "UPSP168586",
        "UPSP169634",
        "UPSP170498",
        "UPSP170507",
        "UPSP170523",
        "UPSP170662",
        "UPSP195329",
        "UPSP196459",
        "UPSP196484",
        "UPSP197348",
        "UPSP197351",
        "UPSP197377",
        "UPSP206555",
        "UPSP213033",
        "UPSP513811",
        "UPSP513939",
        "UPSP514407",
        "UPSP630656",
        "UPSP631802",
        "UPSP631810",
        "UPSP631811",
        "UPSP631817",
        "UPSP632990",
        "UPSP632993",
        "UPSP633063",
        "UPSP633072",
        "UPSP633098",
        "UPSP633129",
        "UPSP633275",
        "UPSP633341",
        "UPSP633351",
        "UPSP633370",
        "UPSP633372",
        "UPSP633411",
        "UPSP634379",
        "UPSP634400",
        "UPSP634923",
        "UPSP634951",
        "UPSP635407",
        "UPSP636294",
        "UPSP666432",
        "UPSP673221",
        "UPSP675102",
        "UPSP676151",
        "UPSP676156",
        "UPSP676167",
        "UPSP676242",
        "UPSP692804",
        "UPSP692813",
        "UPSP692861",
        "UPSP692987",
        "UPSP693542",
        "UPSP693609",
        "UPSP693871",
        "UPSP695592",
        "UPSP699162",
        "UPSP851342",
        "UPSP851435",
        "UPSP852546",
        "UPSP855023",
        "UPSP855027",
        "UPSP855040",
        "UPSP855058",
        "UPSP863988",
        "UPSP865960",
        "UPSP866138",
        "UPSP_1f58",
        "kaveh-testcar2",
        "kaveh-testcar3",
        "test",
    ]

    @task
    def end_to_end_internal(self):
        ### Apply Internal Settings
        logging.info("Apply Internal Settings API...")
        for deviceID in self.device_ids:
            logging.info("Request counter: %d,", self.request_counter)
            if self.request_counter >= self.total_requests:
                logging.info(
                    "Stop the Locust instance once the desired number of requests %d is reached",
                    self.request_counter,
                )
                self.environment.runner.quit()
            try:
                json_file_path = "data/all_external_settings_single.json"
                with open(json_file_path, "r", encoding="ascii") as j:
                    contents = json.loads(j.read())
                payload = contents
                payload["deviceIds"] = [deviceID]
                logging.info("Got deviceID: %s", deviceID)
                headers = {"Content-Type": "application/json"}
                with self.client.patch(
                    "/ext/api/v1/applySettingsExternal",
                    json=payload,
                    headers=headers,
                    catch_response=True,
                ) as response:
                    logging.info("Apply External Settings Response: %s", response)
                    if response.status_code != 204:
                        logging.error(
                            "Unexpected status code: %d", response.status_code
                        )
                        response.failure(
                            f"Failure to execute Apply External Settings API due to Status Code: {response.status_code}"
                        )
                        raise AssertionError("Expecting 204 status code!")
                self.request_counter += 1
                logging.info("Request executed: %d", self.request_counter)
            except AssertionError as e:
                logging.error("An error occurred: %s", e)
