import json
from locust import events
from locust import between, task, SequentialTaskSet, HttpUser


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
    def get_settings(self):
        """Get Settings"""
        with self.client.get(
            "/gwSettings?cartype=P10&facility=PABTN", catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(
                    "Failed to Get Settings, StatusCode: " + str(response.status_code)
                )
            else:
                if "carType" in response.text:
                    response.success()
                else:
                    response.failure("Failed to Get Settings, Text: " + response.text)

    @task
    def apply_settings(self):
        """Apply Settings"""
        hdrs = {"Content-Type": "application/json"}
        payload = {"facility": "PABTN", "carType": "P10"}

        with self.client.post(
            "/applyGwSettings",
            data=json.dumps(payload),
            headers=hdrs,
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    "Failed to Apply Settings, StatusCode: " + str(response.status_code)
                )
            else:
                if "Settings applied successfully" in response.text:
                    response.success()
                else:
                    response.failure("Failed to Apply Settings, Text: " + response.text)

    @task
    def insert_settings(self):
        """Insert Settings"""
        json_file_path = "data/insert_p10.json"
        # json_file_path = "/mnt/locust/data/insert_p10.json"

        with open(json_file_path, "r", encoding="ascii") as j:
            contents = json.loads(j.read())
        payload = contents
        hdrs = {"Content-type": "application/json"}

        with self.client.post(
            "/gwSettings", data=json.dumps(payload), headers=hdrs, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(
                    "Failed to Insert Settings, StatusCode: "
                    + str(response.status_code)
                )
            else:
                if (
                    "Item already exists for Facility: PABTN || carType: P10"
                    in response.text
                ):
                    response.success()
                else:
                    response.failure(
                        "Failed to Insert Settings, Text: " + response.text
                    )

    @task
    def exit_navigation(self):
        self.interrupt()


class MyUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [SPSFLoad]
