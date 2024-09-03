"""locustfile.py"""

import json
import logging
from locust import events
from locust import HttpUser, task, between


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


class SettingUser(HttpUser):
    """Class: SettingUser"""

    wait_time = between(1, 5)
    HOST = "https://trk-spsf-dev-test.azure-api.net"

    @task
    def get_settings(self):
        """Get Settings"""
        resp = self.client.get(self.HOST + "/gwSettings?cartype=P10&facility=PABTN")
        status_code = resp.status_code
        print(f"Status Code: {status_code}")
        try:
            assert status_code == 200
            logging.info("Get Settings, PASSED!")
        except AssertionError:
            logging.error("Get Settings, FAILED!")

    @task
    def apply_settings(self):
        """Apply Settings"""
        hdrs = {"Content-Type": "application/json"}
        payload = {"facility": "PABTN", "carType": "P10"}

        resp = self.client.post(
            self.HOST + "/applyGwSettings",
            data=json.dumps(payload),
            headers=hdrs,
        )
        status_code = resp.status_code
        print(f"Status Code: {status_code}")
        try:
            assert status_code == 200
            logging.info("Apply Settings, PASSED!")
        except AssertionError:
            logging.error("Apply Settings, FAILED!")

    @task
    def insert_settings(self):
        """Insert Settings"""
        json_file_path = "data/insert_p10.json"

        with open(json_file_path, "r", encoding="ascii") as j:
            contents = json.loads(j.read())
        payload = contents
        hdrs = {"Content-type": "application/json"}

        resp = self.client.post(
            self.HOST + "/gwSettings",
            data=json.dumps(payload),
            headers=hdrs,
        )
        status_code = resp.status_code
        print(f"Status Code: {status_code}")
        try:
            assert status_code == 200
            logging.info("Insert Settings, PASSED!")
        except AssertionError:
            logging.error("Insert Settings, FAILED!")

    # @task
    # def update_settings(self):
    #     """Update Settings"""
    #     json_file_path = "data/update.json"

    #     with open(json_file_path, "r", encoding="ascii") as j:
    #         contents = json.loads(j.read())
    #     payload = contents
    #     hdrs = {"Content-type": "application/json"}

    #     resp = self.client.put(
    #         self.HOST + "/gwSettings",
    #         data=json.dumps(payload),
    #         headers=hdrs,
    #     )
    #     status_code = resp.status_code
    #     print(f"Status Code: {status_code}")
    #     try:
    #         assert status_code == 200
    #         logging.info("Update Settings, PASSED!")
    #     except AssertionError:
    #         logging.error("Update Settings, FAILED!")
