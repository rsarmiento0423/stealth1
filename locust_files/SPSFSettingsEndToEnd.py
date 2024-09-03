"""SPSFSettingsEndToEnd.py"""

import json
import logging
import random
from locust import events
from locust import between, task, SequentialTaskSet, HttpUser

# Configure logging
log_file_path = "locust_end-to-end_log.log"

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


def randomCarID():
    car_list = ["kaveh-testcar2", "kaveh-testcar3"]
    return random.choice(car_list)


def randomInteger1():
    """Function: randomInteger"""
    return random.randint(0, 4000)


class SPSFLoad(SequentialTaskSet):
    """Class: SPSFLoad"""

    @task(1)
    def end_to_end_internal_1tapeid(self):
        deviceId = randomDeviceID()

        ### Apply Internal Settings
        logging.info("Apply Internal Settings API for deviceID: %s", deviceId)
        headers = {"Content-Type": "application/json"}
        payload = {
            "tapeIds": [deviceId],
            "patch": {
                "ACTIVE_TIME_MCU": 300,
                "ALTERNATOR_VOLTAGE_TH": 400,
                "APIGEE_AUTH": "SmRxSTNKdUpUMTVoOUVWVGI0aTd5TGlNMTRENHdISzlJWTVjZEFMc3BoMXhVaHU3OnpZVGRKcmdNR2NCcFMwTThhUUd4ZU5FdElXQThWeTV1SWpzVWRxdXF1S01xT3kzcTBTMkxoNm5FNG5LZ0wySnE=",
                "APIGEE_CLIENT_ID": "X59So0zagJhF139t6K5ngi4gRDBFq08lHOwWq526GcJRLquq",
                "BACKUP_INTERVAL": 10,
                "BACKUP_PLAN": 1,
                "BACKUP_TAG": 1,
                "BLE_HEARTBEAT_TIMEOUT_SEC": 360,
                "BLE_MOTION_TIMEOUT_SEC": 300,
                "BLE_SCAN_TIME_SEC": 40,
                "BLE_STOP_MOTION_SEC": 30,
                "CALIBRATION_MODE": 0,
                "CENTER_CODE": "0000",
                "CURL_PROXY_API": "null",
                "CURL_PROXY_CREDENTIAL": "null",
                "CURL_REQUEST_TIMEOUT": 30,
                "END_TIME_MCU": 1600,
                "FACTORY_STANDBY_TIMEOUT_SECS": 3600,
                "FORCE_PROXY_CONFIG": 1,
                "GET_CONFIG_WLAN_CURL_FAILURE_MAX": 10,
                "GET_CONFIG_WLAN_CURL_FAILURE_TIMEOUT_SECS": 900,
                "GET_CONFIG_INTERVAL_SEC": 120,
                "HEARTBEAT_INTERVAL_SEC": 300,
                "HMI_INTERVAL_INVENTORY_MSEC": 0,
                "HMI_INTERVAL_MISLOAD_MSEC": 400,
                "IN_HOUSE_TEST": 0,
                "INACTIVE_SUSPEND_WAIT": 18000,
                "LOAD_SEND_MSG_DELAY_MSEC": 10,
                "LOG_LEVEL": 1,
                "LOOKBACK_PLAN_DAYS": 1,
                "LOW_BATT_POWERON_VOLT": 1050,
                "LOW_BATT_SHUTDOWN_VOLT": 980,
                "MANIFEST_REQ_INTERVAL_SEC": 30,
                "MCU_KEEPALIVE_INTERVAL": 901,
                "MCU_LOG_LEVEL": 1,
                "MCU_LOG_REQ_SEC": 120,
                "MDM_DEBUG_ENABLE": 1,
                "MDM_DEBUG_SERVER": "dbug.trackonomysystems.com",
                "MDM_DEBUG_OUT_PORT": 443,
                "MDM_DEBUG_TLS_SERVER": "dbug.trackonomysystems.com",
                "MIN_TIME_JUMP_TH_SEC": 10,
                "MISLOAD_ACK_BUZZ": 1,
                "MISLOAD_ACK_BUZZ_TIMEOUT_MSEC": 750,
                "MISLOAD_TAG_SEEN_THR": 1,
                "MTLS_FLAGS_WLAN0": 4,
                "MTLS_FLAGS_WWAN0": 4,
                "ON_ROAD_COMM_TYPE": 2,
                "ONROAD_BATTERY_DETECTION": 1,
                "ONROAD_CAR_MOVING_DUR_THR_SEC": 30,
                "ONROAD_CAR_STOP_DUR_THR_SEC": 30,
                "ONROAD_GEN2_Q_1": -1,
                "ONROAD_INACTIVE_SUSPEND_WAIT": 18000,
                "ONROAD_MILLER_CODING_1": 4,
                "ONROAD_READ_POWER_1": 30,
                "ONROAD_RFID_FIRST_SCAN_MULTIPLIER": 2,
                "ONROAD_RFID_SCAN_DUR_SEC": 100,
                "ONROAD_RFID_SLEEP_DUR_SEC": 30,
                "ONROAD_SESSION_1": 2,
                "ONROAD_SPEED_DETECTION": 1,
                "ONROAD_TARGET_1": 3,
                "ONROAD_WRITE_POWER_1": 30,
                "PACKAGE_CAR_SPEED_MAX_TH": 15,
                "PACKAGE_CAR_SPEED_MIN_TH": 3,
                "PACKAGE_RESEND_TIMER_SEC": 30,
                "PIR_ANALOG_EN": 4,
                "PIR_DP_1M_W1": 127,
                "PIR_DP_1M_W2": 127,
                "PIR_LED_EN": 0,
                "PIR_LOCK_TIME_SEC": 2,
                "PIR_MISLOAD_DETECTION": 1,
                "PIR_MISLOAD_RETRY_MSEC": 1500,
                "PIR_MODE": 0,
                "PIR_REF_VOLTAGE_LOW": 100,
                "PIR_REF_VOLTAGE_HIGH": 105,
                "PIR_SELECT_TIMEOUT_USEC": 50,
                "PIR_SLEEP_TIME_MSECS": 20,
                "PRELOAD_START_TIME": 1000,
                "PUSH_SUMMARY_STATS_TIMER": 1801,
                "PUSH_TAG_STATS_TIMER": 0,
                "RESEND_MAX_PACKET_COUNT": 3,
                "RETRY_WAKE_TIME_MCU": 910,
                "RFID_1A_FILTER": 1,
                "RFID_ANTENNA_1": 1,
                "RFID_GEN2_Q_1": -1,
                "RFID_MILLER_CODING_1": 3,
                "RFID_READER": 1,
                "RFID_READ_POWER_1": 14,
                "RFID_REGION_INDEX_1": 1,
                "RFID_SESSION_1": 1,
                "RFID_TAG_SEARCH_TIMES_1": 250,
                "RFID_TARGET_1": 0,
                "RFID_WRITE_POWER_1": 14,
                "RSSI_THRESHOLD_INVENTORY": 0,
                "RSSI_THRESHOLD_MISLOAD": 59,
                "SECTIGO_CERT_EXPIRY_BUFFER_DAYS": 30,
                "SECTIGO_CERT_VALIDATION_INTERVAL": 21600,
                "SECTIGO_CERT_TERM": "365",
                "SECTIGO_CERT_TYPE": "1439",
                "SECTIGO_CUSTOMER_URI": "ups",
                "SECTIGO_LOGIN": "trackonomy",
                "SECTIGO_ORG_ID": "3505",
                "SECTIGO_PASSWORD": "H3lpfull!!)@**",
                "SOM_IN_SUSPEND_DUR": 120,
                "SOM_SHUTDOWN_MODE": 1,
                "SPSF_ENABLE_SECURE_DEBUG": 2,
                "STATUS_INTERVAL_SEC": 900,
                "STOP_CUSTOMER_COMM": 0,
                "SYSTEM_RESET_FLAG": 0,
                "TARGET_READ_BOOST_END_TIME": "1430",
                "TARGET_READ_BOOST_MULTIPLIER": 5,
                "TARGET_READ_BOOST_START_TIME": "1145",
                "TARGET_READ_DUR_SEC": 30,
                "TARGET_READ_END_TIME": "2359",
                "TARGET_READ_INTERVAL_MINS": 30,
                "TARGET_READ_START_TIME": "2359",
                "UART_MSG_COMM_TYPE": 1,
                "UART_MSG_RETRY_SEC": 20,
                "UART_MSG_TIMEOUT_MS": 250,
                "URL_APIGEE_GET_OAUTH_TOKEN": "https://onlinetools.ups.com/ent-services/security/v1/oauth/token",
                "URL_BLE": "https://trk-spsf-prd.azure-api.net/v2/prox",
                "URL_GET_PACKAGE_CAR": "https://trk-spsf-prd.azure-api.net/v2/rfidGetPkgcar?gwId=",
                "URL_HEARTBEAT": "https://trk-spsf-prd.azure-api.net/v2/heartbeat",
                "URL_MANIFEST_WLAN": "https://onlinetools.ups.com/ent-services/package-operations/v1/rfid/packages/",
                "URL_MANIFEST_WWAN": "https://onlinetools.ups.com/ent-services/package-operations/v1/rfid/packages/",
                "URL_MDM_DEBUG_IN_PORT": "https://trk-spsf-prd.azure-api.net/v2/lookup-port?macid=",
                "URL_ONROAD_STATS": "https://trk-spsf-prd.azure-api.net/v2/events/on-road",
                "URL_PACKAGE_TRANS_WLAN": "https://onlinetools.ups.com/ent-services/package-operations/v1/rfid/packageTransition/",
                "URL_PACKAGE_TRANS_WWAN": "https://onlinetools.ups.com/ent-services/package-operations/v1/rfid/packageTransition/",
                "URL_PLAN_STATS": "https://trk-spsf-prd.azure-api.net/association/manifest",
                "URL_SERVER_TIME": "https://trk-spsf-prd.azure-api.net/v2/rfidGetCurUTCTime",
                "URL_STATUS_WLAN": "https://onlinetools.ups.com/ent-services/package-operations/v1/rfid/status/",
                "URL_STATUS_WWAN": "https://onlinetools.ups.com/ent-services/package-operations/v1/rfid/status/",
                "URL_SUMMARY_STATS": "https://trk-spsf-prd.azure-api.net/v2/addStats?id=",
                "URL_TAG_STATS": "https://trk-spsf-prd.azure-api.net/inventory/preload",
                "URL_GET_TRK_OTA": "https://trk-spsf-prd.azure-api.net/ota/status?id=",
                "URL_GET_OTA_STATUS": "https://trk-spsf-prd.azure-api.net/ota/lastUpdateStatus",
                "URL_POST_OTA_STATUS": "https://trk-spsf-prd.azure-api.net/ota/updateStatus",
                "URL_SECTIGO_ENROLL": "https://cert-manager.com/api/device/v1/enroll?gwsource=externalsource",
                "URL_SECTIGO_COLLECT": "https://cert-manager.com/api/device/v1/collect/",
                "URL_SET_TRK_OTA": "https://trk-spsf-prd.azure-api.net/ota/statustape",
                "URL_WIFI": "https://trk-spsf-prd.azure-api.net/wifi/v3/wifiEncrypted?macId=",
                "WATCHDOG_INTERVAL_SEC": 300,
                "WLAN_CURL_FAILURE_MAX": 6,
                "WLAN_CURL_FAILURE_TIMEOUT_SECS": 180,
                "URL_GET_CONFIG_DIFF_ZIP": "https://trk-spsf-prd.azure-api.net/v2/getsettingsdiff?id=",
                "URL_GET_CONFIG_ALL_ZIP": "https://trk-spsf-prd.azure-api.net/v2/getsettingscompressed?id=",
                "URL_GET_CONFIG_DIFF_ACK": "https://trk-spsf-prd.azure-api.net/v2/settingsAcknowledge",
                "ACC_X_TH": 6,
                "ACC_X_TH2": 5,
                "RSSI_THRESHOLD_IN": 55,
                "RSSI_TH_CHANGE": 0,
                "PIR_TEMP_ADJ_REF_VOLTAGE_HIGH": 60,
                "PIR_TEMP_ADJ_REF_VOLTAGE_LOW": 60,
                "EXT_HOSTS_UPDATE": 0,
                "ADPT_MISL_PATTERN_ACT_1": 1,
                "ADPT_MISL_PATTERN_ACT_2": 2,
                "ADPT_MISL_PATTERN_ACT_3": 3,
                "ADPT_MISL_PATTERN_ACT_4": 0,
                "ADPT_MISL_PATTERN_ACT_5": 0,
                "ADPT_INV_COUNT_TX_POWER_1": 100,
                "ADPT_INV_COUNT_TX_POWER_2": 200,
                "ADPT_INV_COUNT_TX_POWER_3": 0,
                "ADPT_INV_COUNT_TX_POWER_4": 0,
                "ADPT_INV_COUNT_TX_POWER_5": 0,
                "ADPT_INV_COUNT_RX_POWER_1": 50,
                "ADPT_INV_COUNT_RX_POWER_2": 150,
                "ADPT_INV_COUNT_RX_POWER_3": 0,
                "ADPT_INV_COUNT_RX_POWER_4": 0,
                "ADPT_INV_COUNT_RX_POWER_5": 0,
                "ADPT_INV_COUNT_TX_POWER_RSSI_1": 59,
                "ADPT_INV_COUNT_TX_POWER_RSSI_2": 58,
                "ADPT_INV_COUNT_TX_POWER_RSSI_3": 0,
                "ADPT_INV_COUNT_TX_POWER_RSSI_4": 0,
                "ADPT_INV_COUNT_TX_POWER_RSSI_5": 0,
                "ADPT_INV_COUNT_RX_POWER_RSSI_1": 0,
                "ADPT_INV_COUNT_RX_POWER_RSSI_2": 0,
                "ADPT_INV_COUNT_RX_POWER_RSSI_3": 0,
                "ADPT_INV_COUNT_RX_POWER_RSSI_4": 0,
                "ADPT_INV_COUNT_RX_POWER_RSSI_5": 0,
                "ADPT_MISL_PATTERN_COUNT": 15,
                "ADPT_MISL_PATTERN_SECS": 1800,
                "MAX_APP_RESET_COUNT": 3,
                "MAX_APP_RESET_DUR_SEC": 900,
                "MAX_SOM_RESET_COUNT": 3,
                "MAX_SOM_RESET_DUR_SEC": 900,
                "ON_DEMAND_SCAN": 0,
                "ON_DEMAND_SCAN_DUR_SEC": 0,
                "UPLOAD_LOG_MIN": 0,
                "SELF_TEST": 0,
            },
        }
        logging.info("Got updated payload: %s", payload)
        with self.client.patch(
            "/api/v1/applySettings", json=payload, headers=headers, catch_response=True
        ) as response:
            logging.info("Response: %s", response)
            if response.status_code != 204:
                response.failure(
                    "Failure to execute Apply Internal Settings API due to Status Code: "
                    + str(response.status_code)
                )

        ### Get Package Car Settings Diff
        logging.info("Get Package Car Settings Diff API for deviceID: %s", deviceId)
        with self.client.get(
            "/pkgCarSettingsDiff?id=" + deviceId, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(
                    "Failure to execute Get Package Car Settings Diff API due to Status Code: "
                    + str(response.status_code)
                )
            elif "ackUuid" in response.text:
                response.success()
                response_data = json.loads(response.text)
                ACTUAL_ackUuID = response_data[0]["ackUuid"]
                ACTUAL_ACTIVE_TIME_MCU = response_data[0]["settings"]["ACTIVE_TIME_MCU"]
                ACTUAL_ALTERNATOR_VOLTAGE_TH = response_data[0]["settings"][
                    "ALTERNATOR_VOLTAGE_TH"
                ]
                assert ACTUAL_ACTIVE_TIME_MCU == 300
                assert ACTUAL_ALTERNATOR_VOLTAGE_TH == 400
                assert len(response_data[0]["settings"]) == 189
                logging.info(
                    "Got Package Car Settings Diff Actual ackUuid: %s", ACTUAL_ackUuID
                )
            else:
                response.failure(
                    "Expected response from Package Car Settings Diff API!"
                )

        ### Get Package Car Ack
        logging.info("Get Package Car Ack API for deviceID: %s", deviceId)
        payload = {"ackUuid": ACTUAL_ackUuID}
        headers = {"Content-Type": "application/json"}
        with self.client.post(
            "/pkgCarSettingsAck", json=payload, headers=headers, catch_response=True
        ) as response:
            logging.info("Get Package Car Ack Response %s:", response)
            if response.status_code != 200:
                response.failure(
                    "Failure to execute Get Package Car Ack API due to Status Code: "
                    + str(response.status_code)
                )

        ### Get Package Car Settings Diff and verify settings object is 0
        logging.info("Get Package Car Settings Diff API for deviceID: %s", deviceId)
        with self.client.get(
            "/pkgCarSettingsDiff?id=" + deviceId, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(
                    "Failure to execute Get Package Car Settings Diff API due to Status Code: "
                    + str(response.status_code)
                )
            elif "ackUuid" in response.text:
                response.success()
                response_data = json.loads(response.text)
                ACTUAL_ackUuID = response_data[0]["ackUuid"]
                assert len(response_data[0]["settings"]) == 0
                logging.info(
                    "Got Package Car Settings Diff Actual ackUuid: %s", ACTUAL_ackUuID
                )
            else:
                response.failure(
                    "Expected response from Package Car Settings Diff API!"
                )

        ### Get Package Car Settings
        logging.info("Get Settings API for deviceID: %s", deviceId)
        with self.client.get(
            "/pkgCarSettings?id=" + deviceId, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(
                    "Failure to execute Get Package Car Settings API due to Status Code: "
                    + str(response.status_code)
                )
            elif "ackUuid" in response.text:
                response_data = json.loads(response.text)
                ackUuID = response_data[0]["ackUuid"]
                logging.info("Got Get Package Car Settings ackUuid: %s", ackUuID)
                response.success()
            else:
                response.failure("Expected response from Get Package Car Settings API!")

    @task(0)
    def end_to_end_internal_110tapeids(self):

        ### Apply Internal Settings
        logging.info("Apply Internal Settings API for 110 deviceIDs")
        headers = {"Content-Type": "application/json"}
        payload = {
            "tapeIds": [
                "001f7b3f1cdc",
                "001f7b3f1d00",
                "001f7b3f1d0c",
                "001f7b3f1d1e",
                "001f7b3f1d22",
                "001f7b3f1d3a",
                "001f7b3f1d3c",
                "001f7b3f1d5c",
                "001f7b3f1db4",
                "001f7b3f1dc2",
                "001f7b3f1e8e",
                "001f7b3f1eb2",
                "001f7b3f1f58",
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
                "001f7b3fc784",
                "001f7b3fc786",
                "001f7b3fc788",
                "001f7b3fc78a",
                "001f7b3fc79e",
                "001f7b3fc7d8",
                "001f7b3fc7da",
                "001f7b3fc7e2",
                "001f7b3fc7e8",
                "001f7b3fc7fe",
                "001f7b3fc802",
                "001f7b3fc808",
                "001f7b3fc80a",
                "001f7b3fc80c",
                "001f7b3fc812",
                "001f7b3fc816",
                "001f7b3fc81a",
                "001f7b3fc824",
                "001f7b3fc82a",
                "001f7b3fc830",
                "001f7b3fc834",
                "001f7b3fc83a",
                "001f7b3fc83c",
                "001f7b3fc842",
            ],
            "patch": {
                "ACTIVE_TIME_MCU": 300,
                "ALTERNATOR_VOLTAGE_TH": 400,
                "APIGEE_AUTH": "SmRxSTNKdUpUMTVoOUVWVGI0aTd5TGlNMTRENHdISzlJWTVjZEFMc3BoMXhVaHU3OnpZVGRKcmdNR2NCcFMwTThhUUd4ZU5FdElXQThWeTV1SWpzVWRxdXF1S01xT3kzcTBTMkxoNm5FNG5LZ0wySnE=",
                "APIGEE_CLIENT_ID": "X59So0zagJhF139t6K5ngi4gRDBFq08lHOwWq526GcJRLquq",
                "BACKUP_INTERVAL": 10,
                "BACKUP_PLAN": 1,
                "BACKUP_TAG": 1,
                "BLE_HEARTBEAT_TIMEOUT_SEC": 360,
                "BLE_MOTION_TIMEOUT_SEC": 300,
                "BLE_SCAN_TIME_SEC": 40,
                "BLE_STOP_MOTION_SEC": 30,
                "CALIBRATION_MODE": 0,
                "CENTER_CODE": "0000",
                "CURL_PROXY_API": "null",
                "CURL_PROXY_CREDENTIAL": "null",
                "CURL_REQUEST_TIMEOUT": 30,
                "END_TIME_MCU": 1600,
                "FACTORY_STANDBY_TIMEOUT_SECS": 3600,
                "FORCE_PROXY_CONFIG": 1,
                "GET_CONFIG_WLAN_CURL_FAILURE_MAX": 10,
                "GET_CONFIG_WLAN_CURL_FAILURE_TIMEOUT_SECS": 900,
                "GET_CONFIG_INTERVAL_SEC": 120,
                "HEARTBEAT_INTERVAL_SEC": 300,
                "HMI_INTERVAL_INVENTORY_MSEC": 0,
                "HMI_INTERVAL_MISLOAD_MSEC": 400,
                "IN_HOUSE_TEST": 0,
                "INACTIVE_SUSPEND_WAIT": 18000,
                "LOAD_SEND_MSG_DELAY_MSEC": 10,
                "LOG_LEVEL": 1,
                "LOOKBACK_PLAN_DAYS": 1,
                "LOW_BATT_POWERON_VOLT": 1050,
                "LOW_BATT_SHUTDOWN_VOLT": 980,
                "MANIFEST_REQ_INTERVAL_SEC": 30,
                "MCU_KEEPALIVE_INTERVAL": 901,
                "MCU_LOG_LEVEL": 1,
                "MCU_LOG_REQ_SEC": 120,
                "MDM_DEBUG_ENABLE": 1,
                "MDM_DEBUG_SERVER": "dbug.trackonomysystems.com",
                "MDM_DEBUG_OUT_PORT": 443,
                "MDM_DEBUG_TLS_SERVER": "dbug.trackonomysystems.com",
                "MIN_TIME_JUMP_TH_SEC": 10,
                "MISLOAD_ACK_BUZZ": 1,
                "MISLOAD_ACK_BUZZ_TIMEOUT_MSEC": 750,
                "MISLOAD_TAG_SEEN_THR": 1,
                "MTLS_FLAGS_WLAN0": 4,
                "MTLS_FLAGS_WWAN0": 4,
                "ON_ROAD_COMM_TYPE": 2,
                "ONROAD_BATTERY_DETECTION": 1,
                "ONROAD_CAR_MOVING_DUR_THR_SEC": 30,
                "ONROAD_CAR_STOP_DUR_THR_SEC": 30,
                "ONROAD_GEN2_Q_1": -1,
                "ONROAD_INACTIVE_SUSPEND_WAIT": 18000,
                "ONROAD_MILLER_CODING_1": 4,
                "ONROAD_READ_POWER_1": 30,
                "ONROAD_RFID_FIRST_SCAN_MULTIPLIER": 2,
                "ONROAD_RFID_SCAN_DUR_SEC": 100,
                "ONROAD_RFID_SLEEP_DUR_SEC": 30,
                "ONROAD_SESSION_1": 2,
                "ONROAD_SPEED_DETECTION": 1,
                "ONROAD_TARGET_1": 3,
                "ONROAD_WRITE_POWER_1": 30,
                "PACKAGE_CAR_SPEED_MAX_TH": 15,
                "PACKAGE_CAR_SPEED_MIN_TH": 3,
                "PACKAGE_RESEND_TIMER_SEC": 30,
                "PIR_ANALOG_EN": 4,
                "PIR_DP_1M_W1": 127,
                "PIR_DP_1M_W2": 127,
                "PIR_LED_EN": 0,
                "PIR_LOCK_TIME_SEC": 2,
                "PIR_MISLOAD_DETECTION": 1,
                "PIR_MISLOAD_RETRY_MSEC": 1500,
                "PIR_MODE": 0,
                "PIR_REF_VOLTAGE_LOW": 100,
                "PIR_REF_VOLTAGE_HIGH": 105,
                "PIR_SELECT_TIMEOUT_USEC": 50,
                "PIR_SLEEP_TIME_MSECS": 20,
                "PRELOAD_START_TIME": 1000,
                "PUSH_SUMMARY_STATS_TIMER": 1801,
                "PUSH_TAG_STATS_TIMER": 0,
                "RESEND_MAX_PACKET_COUNT": 3,
                "RETRY_WAKE_TIME_MCU": 910,
                "RFID_1A_FILTER": 1,
                "RFID_ANTENNA_1": 1,
                "RFID_GEN2_Q_1": -1,
                "RFID_MILLER_CODING_1": 3,
                "RFID_READER": 1,
                "RFID_READ_POWER_1": 14,
                "RFID_REGION_INDEX_1": 1,
                "RFID_SESSION_1": 1,
                "RFID_TAG_SEARCH_TIMES_1": 250,
                "RFID_TARGET_1": 0,
                "RFID_WRITE_POWER_1": 14,
                "RSSI_THRESHOLD_INVENTORY": 0,
                "RSSI_THRESHOLD_MISLOAD": 59,
                "SECTIGO_CERT_EXPIRY_BUFFER_DAYS": 30,
                "SECTIGO_CERT_VALIDATION_INTERVAL": 21600,
                "SECTIGO_CERT_TERM": "365",
                "SECTIGO_CERT_TYPE": "1439",
                "SECTIGO_CUSTOMER_URI": "ups",
                "SECTIGO_LOGIN": "trackonomy",
                "SECTIGO_ORG_ID": "3505",
                "SECTIGO_PASSWORD": "H3lpfull!!)@**",
                "SOM_IN_SUSPEND_DUR": 120,
                "SOM_SHUTDOWN_MODE": 1,
                "SPSF_ENABLE_SECURE_DEBUG": 2,
                "STATUS_INTERVAL_SEC": 900,
                "STOP_CUSTOMER_COMM": 0,
                "SYSTEM_RESET_FLAG": 0,
                "TARGET_READ_BOOST_END_TIME": "1430",
                "TARGET_READ_BOOST_MULTIPLIER": 5,
                "TARGET_READ_BOOST_START_TIME": "1145",
                "TARGET_READ_DUR_SEC": 30,
                "TARGET_READ_END_TIME": "2359",
                "TARGET_READ_INTERVAL_MINS": 30,
                "TARGET_READ_START_TIME": "2359",
                "UART_MSG_COMM_TYPE": 1,
                "UART_MSG_RETRY_SEC": 20,
                "UART_MSG_TIMEOUT_MS": 250,
                "URL_APIGEE_GET_OAUTH_TOKEN": "https://onlinetools.ups.com/ent-services/security/v1/oauth/token",
                "URL_BLE": "https://trk-spsf-prd.azure-api.net/v2/prox",
                "URL_GET_PACKAGE_CAR": "https://trk-spsf-prd.azure-api.net/v2/rfidGetPkgcar?gwId=",
                "URL_HEARTBEAT": "https://trk-spsf-prd.azure-api.net/v2/heartbeat",
                "URL_MANIFEST_WLAN": "https://onlinetools.ups.com/ent-services/package-operations/v1/rfid/packages/",
                "URL_MANIFEST_WWAN": "https://onlinetools.ups.com/ent-services/package-operations/v1/rfid/packages/",
                "URL_MDM_DEBUG_IN_PORT": "https://trk-spsf-prd.azure-api.net/v2/lookup-port?macid=",
                "URL_ONROAD_STATS": "https://trk-spsf-prd.azure-api.net/v2/events/on-road",
                "URL_PACKAGE_TRANS_WLAN": "https://onlinetools.ups.com/ent-services/package-operations/v1/rfid/packageTransition/",
                "URL_PACKAGE_TRANS_WWAN": "https://onlinetools.ups.com/ent-services/package-operations/v1/rfid/packageTransition/",
                "URL_PLAN_STATS": "https://trk-spsf-prd.azure-api.net/association/manifest",
                "URL_SERVER_TIME": "https://trk-spsf-prd.azure-api.net/v2/rfidGetCurUTCTime",
                "URL_STATUS_WLAN": "https://onlinetools.ups.com/ent-services/package-operations/v1/rfid/status/",
                "URL_STATUS_WWAN": "https://onlinetools.ups.com/ent-services/package-operations/v1/rfid/status/",
                "URL_SUMMARY_STATS": "https://trk-spsf-prd.azure-api.net/v2/addStats?id=",
                "URL_TAG_STATS": "https://trk-spsf-prd.azure-api.net/inventory/preload",
                "URL_GET_TRK_OTA": "https://trk-spsf-prd.azure-api.net/ota/status?id=",
                "URL_GET_OTA_STATUS": "https://trk-spsf-prd.azure-api.net/ota/lastUpdateStatus",
                "URL_POST_OTA_STATUS": "https://trk-spsf-prd.azure-api.net/ota/updateStatus",
                "URL_SECTIGO_ENROLL": "https://cert-manager.com/api/device/v1/enroll?gwsource=externalsource",
                "URL_SECTIGO_COLLECT": "https://cert-manager.com/api/device/v1/collect/",
                "URL_SET_TRK_OTA": "https://trk-spsf-prd.azure-api.net/ota/statustape",
                "URL_WIFI": "https://trk-spsf-prd.azure-api.net/wifi/v3/wifiEncrypted?macId=",
                "WATCHDOG_INTERVAL_SEC": 300,
                "WLAN_CURL_FAILURE_MAX": 6,
                "WLAN_CURL_FAILURE_TIMEOUT_SECS": 180,
                "URL_GET_CONFIG_DIFF_ZIP": "https://trk-spsf-prd.azure-api.net/v2/getsettingsdiff?id=",
                "URL_GET_CONFIG_ALL_ZIP": "https://trk-spsf-prd.azure-api.net/v2/getsettingscompressed?id=",
                "URL_GET_CONFIG_DIFF_ACK": "https://trk-spsf-prd.azure-api.net/v2/settingsAcknowledge",
                "ACC_X_TH": 6,
                "ACC_X_TH2": 5,
                "RSSI_THRESHOLD_IN": 55,
                "RSSI_TH_CHANGE": 0,
                "PIR_TEMP_ADJ_REF_VOLTAGE_HIGH": 60,
                "PIR_TEMP_ADJ_REF_VOLTAGE_LOW": 60,
                "EXT_HOSTS_UPDATE": 0,
                "ADPT_MISL_PATTERN_ACT_1": 1,
                "ADPT_MISL_PATTERN_ACT_2": 2,
                "ADPT_MISL_PATTERN_ACT_3": 3,
                "ADPT_MISL_PATTERN_ACT_4": 0,
                "ADPT_MISL_PATTERN_ACT_5": 0,
                "ADPT_INV_COUNT_TX_POWER_1": 100,
                "ADPT_INV_COUNT_TX_POWER_2": 200,
                "ADPT_INV_COUNT_TX_POWER_3": 0,
                "ADPT_INV_COUNT_TX_POWER_4": 0,
                "ADPT_INV_COUNT_TX_POWER_5": 0,
                "ADPT_INV_COUNT_RX_POWER_1": 50,
                "ADPT_INV_COUNT_RX_POWER_2": 150,
                "ADPT_INV_COUNT_RX_POWER_3": 0,
                "ADPT_INV_COUNT_RX_POWER_4": 0,
                "ADPT_INV_COUNT_RX_POWER_5": 0,
                "ADPT_INV_COUNT_TX_POWER_RSSI_1": 59,
                "ADPT_INV_COUNT_TX_POWER_RSSI_2": 58,
                "ADPT_INV_COUNT_TX_POWER_RSSI_3": 0,
                "ADPT_INV_COUNT_TX_POWER_RSSI_4": 0,
                "ADPT_INV_COUNT_TX_POWER_RSSI_5": 0,
                "ADPT_INV_COUNT_RX_POWER_RSSI_1": 0,
                "ADPT_INV_COUNT_RX_POWER_RSSI_2": 0,
                "ADPT_INV_COUNT_RX_POWER_RSSI_3": 0,
                "ADPT_INV_COUNT_RX_POWER_RSSI_4": 0,
                "ADPT_INV_COUNT_RX_POWER_RSSI_5": 0,
                "ADPT_MISL_PATTERN_COUNT": 15,
                "ADPT_MISL_PATTERN_SECS": 1800,
                "MAX_APP_RESET_COUNT": 3,
                "MAX_APP_RESET_DUR_SEC": 900,
                "MAX_SOM_RESET_COUNT": 3,
                "MAX_SOM_RESET_DUR_SEC": 900,
                "ON_DEMAND_SCAN": 0,
                "ON_DEMAND_SCAN_DUR_SEC": 0,
                "UPLOAD_LOG_MIN": 0,
                "SELF_TEST": 0,
            },
        }
        logging.info("Got updated payload: %s", payload)
        with self.client.patch(
            "/api/v1/applySettings", json=payload, headers=headers, catch_response=True
        ) as response:
            logging.info("Response: %s", response)
            if response.status_code != 204:
                response.failure(
                    "Failure to execute Apply Internal Settings API for 110 devices due to Status Code: "
                    + str(response.status_code)
                )

    @task(1)
    def end_to_end_external_1deviceid(self):
        carID = "kaveh-testcar3"
        deviceId = "001f7b3f2094"

        ### Apply External Settings
        logging.info("Apply External Settings API for carID: %s", carID)
        headers = {"Content-Type": "application/json"}
        payload = {
            "correlationId": "191919192",
            "deviceIds": [carID],
            "patch": {
                "ON_DEMAND_SCAN": 1,
                "ON_DEMAND_SCAN_DUR_SEC": 86400,
                "UPLOAD_LOG_MIN": 43200,
                "SYSTEM_RESET_FLAG": 1,
                "SELF_TEST": 1,
            },
        }
        with self.client.patch(
            "/ext/api/v1/applySettingsExternal",
            json=payload,
            headers=headers,
            catch_response=True,
        ) as response:
            logging.info("Response: %s", response)
            if response.status_code != 204:
                response.failure(
                    "Failure to execute Apply External Settings API due to Status Code: "
                    + str(response.status_code)
                )

        ### Get Package Car Settings Diff
        logging.info("Get Package Car Settings Diff API for deviceID: %s", deviceId)
        with self.client.get(
            "/pkgCarSettingsDiff?id=" + deviceId, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(
                    "Failure to execute Get Package Car Settings Diff API due to Status Code: "
                    + str(response.status_code)
                )
            elif "ackUuid" in response.text:
                response.success()
                response_data = json.loads(response.text)
                ACTUAL_ackUuID = response_data[0]["ackUuid"]
                ACTUAL_ON_DEMAND_SCAN = response_data[0]["settings"]["ON_DEMAND_SCAN"]
                ACTUAL_ON_DEMAND_SCAN_DUR_SEC = response_data[0]["settings"][
                    "ON_DEMAND_SCAN_DUR_SEC"
                ]
                ACTUAL_UPLOAD_LOG_MIN = response_data[0]["settings"]["UPLOAD_LOG_MIN"]
                ACTUAL_SYSTEM_RESET_FLAG = response_data[0]["settings"][
                    "SYSTEM_RESET_FLAG"
                ]
                ACTUAL_SELF_TEST = response_data[0]["settings"]["SELF_TEST"]
                assert ACTUAL_ON_DEMAND_SCAN == 1
                assert ACTUAL_ON_DEMAND_SCAN_DUR_SEC == 86400
                assert ACTUAL_UPLOAD_LOG_MIN == 43200
                assert ACTUAL_SYSTEM_RESET_FLAG == 1
                assert ACTUAL_SELF_TEST == 1
                assert len(response_data[0]["settings"]) == 5
                logging.info(
                    "Got Get Package Car Settings Actual ackUuid: %s", ACTUAL_ackUuID
                )
            else:
                response.failure(
                    "Expected 'ackUuid' in response for Package Car Settings Diff API!"
                )

        ### Get Package Car Ack
        logging.info("Get Package Car Ack API for deviceID: %s", deviceId)
        headers = {"Content-Type": "application/json"}
        payload = {"ackUuid": ACTUAL_ackUuID}
        with self.client.post(
            "/pkgCarSettingsAck", json=payload, headers=headers, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(
                    "Failure to execute Get Package Car Ack API due to Status Code: "
                    + str(response.status_code)
                )

        ### Get Package Car Settings Diff and verify settings object is 0
        logging.info("Get Package Car Settings Diff API for deviceID: %s", deviceId)
        with self.client.get(
            "/pkgCarSettingsDiff?id=" + deviceId, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(
                    "Failure to execute Get Package Car Settings Diff API due to Status Code: "
                    + str(response.status_code)
                )
            elif "ackUuid" in response.text:
                response.success()
                response_data = json.loads(response.text)
                ACTUAL_ackUuID = response_data[0]["ackUuid"]
                assert len(response_data[0]["settings"]) == 0
                logging.info(
                    "Got Package Car Settings Diff Actual ackUuid: %s", ACTUAL_ackUuID
                )
            else:
                response.failure(
                    "Expected response from Package Car Settings Diff API!"
                )

        ### Get Package Car Settings
        logging.info("Get Settings for deviceID: %s", deviceId)
        with self.client.get(
            "/pkgCarSettings?id=" + deviceId, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(
                    "Failure to execute Get Package Car Settings API due to Status Code: "
                    + str(response.status_code)
                )
            elif "ackUuid" in response.text:
                response_data = json.loads(response.text)
                ackUuID = response_data[0]["ackUuid"]
                logging.info("Got Get Package Car Settings ackUuid: %s", ackUuID)
                response.success()
            else:
                response.failure(
                    "Expected 'ackUuid' in response for Get Package Car Settings API!"
                )

    @task(0)
    def end_to_end_external_110deviceids(self):
        ### Apply External Settings
        logging.info("Apply External Settings API for 110 deviceIDs")
        headers = {"Content-Type": "application/json"}
        payload = {
            "correlationId": "191919196",
            "deviceIds": [
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
            ],
            "patch": {
                "ON_DEMAND_SCAN": 1,
                "ON_DEMAND_SCAN_DUR_SEC": 86400,
                "UPLOAD_LOG_MIN": 43200,
                "SYSTEM_RESET_FLAG": 1,
                "SELF_TEST": 1,
            },
        }
        with self.client.patch(
            "/ext/api/v1/applySettingsExternal",
            json=payload,
            headers=headers,
            catch_response=True,
        ) as response:
            logging.info("Response: %s", response)
            if response.status_code != 204:
                response.failure(
                    "Failure to execute Apply External Settings API due to Status Code: "
                    + str(response.status_code)
                )

    @task
    def exit_navigation(self):
        self.interrupt()


class MyUser(HttpUser):
    wait_time = between(7, 10)
    tasks = [SPSFLoad]
