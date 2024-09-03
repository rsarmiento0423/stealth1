""" Package Car Settings Tests """

import os
import json
import pytest
from utils.libs import get_request, patch_request, post_request2


### Package Car Get Settings
@pytest.mark.regression
@pytest.mark.package_car_settings
def test_package_car_get_settings():
    """Get Package Car Settings"""
    deviceID1 = os.environ.get("deviceID1")
    output = get_request("/pkgCarSettings?id=" + deviceID1, 200)
    pkgCarID = output[0]["pkgCarId"]
    ackUuID = output[0]["ackUuid"]
    assert pkgCarID == deviceID1, f"Expected devicID: {deviceID1}!"
    assert len(ackUuID) == 23


### Package Car Get Settings Diff
@pytest.mark.regression
@pytest.mark.package_car_settings
def test_package_car_get_settings_diff():
    """Get Package Car Settings Diff"""
    deviceID1 = os.environ.get("deviceID1")
    output = get_request("/pkgCarSettingsDiff?id=" + deviceID1, 200)
    pkgCarID = output[0]["pkgCarId"]
    ackUuID = output[0]["ackUuid"]
    assert pkgCarID == deviceID1, f"Expected deviceID: {deviceID1}!"
    assert len(ackUuID) == 23


### Package Car Get Settings Ack
@pytest.mark.regression
@pytest.mark.package_car_settings
def test_package_car_get_settings_ack():
    """Get Package Car Ack"""
    deviceID1 = os.environ.get("deviceID1")
    output = get_request("/pkgCarSettings?id=" + deviceID1, 200)
    ackUuID = output[0]["ackUuid"]
    payload = {"ackUuid": ackUuID}
    post_request2("/pkgCarSettingsAck", payload, expected_status=200)


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_package_car_get_settings_ack_empty_ackuuid():
    """Get Package Car Ack Empty ackUuid"""
    payload = {"ackUuid": ""}
    output = post_request2("/pkgCarSettingsAck", payload, expected_status=400)
    error_msg = output["message"]
    assert error_msg == "Invalid ackUuid: expected timestamp. "


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_package_car_get_settings_ack_empty_payload():
    """Get Package Car Ack Empty Payload"""
    payload = {}
    output = post_request2("/pkgCarSettingsAck", payload, expected_status=400)
    error_msg = output["message"]
    assert error_msg == "Invalid ackUuid: expected timestamp. "


## Apply Settings
@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_using_tapeIds():
    """Patch Apply Settings Using tapeIds"""
    deviceID1 = os.environ.get("deviceID1")
    endpoint = "/api/v1/applySettings"
    payload = {
        "tapeIds": [deviceID1],
        "patch": {
            "ACTIVE_TIME_MCU": 350,
            "ALTERNATOR_VOLTAGE_TH": 1500,
            "ON_DEMAND_SCAN": 1,
        },
    }
    expected_status = 204
    patch_request(endpoint, payload, expected_status)


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_using_multiple_tapeIds():
    """Patch Apply Settings Using tapeIds"""
    deviceID1 = os.environ.get("deviceID1")
    deviceID2 = os.environ.get("deviceID2")
    endpoint = "/api/v1/applySettings"
    payload = {
        "tapeIds": [
            deviceID1,
            deviceID2,
        ],
        "patch": {
            "ACTIVE_TIME_MCU": 200,
            "ALTERNATOR_VOLTAGE_TH": 1000,
            "ON_DEMAND_SCAN": 0,
        },
    }
    expected_status = 204
    patch_request(endpoint, payload, expected_status)


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_with_empty_tapeIds():
    """Patch Apply Settings with empty tapeIds"""
    endpoint = "/api/v1/applySettings"
    payload = {
        "tapeIds": [],
        "patch": {
            "ACTIVE_TIME_MCU": 100,
            "ALTERNATOR_VOLTAGE_TH": 1000,
            "ON_DEMAND_SCAN": 0,
        },
    }
    expected_status = 400
    output = patch_request(endpoint, payload, expected_status)
    error_msg = output["msg"]
    assert error_msg == "No device IDs specified."


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_using_facility():
    """Patch Apply Settings Using facility"""
    endpoint = "/api/v1/applySettings"
    payload = {
        "facility": "PABTN",
        "patch": {
            "ACTIVE_TIME_MCU": 400,
            "ALTERNATOR_VOLTAGE_TH": 2000,
            "ON_DEMAND_SCAN": 0,
        },
    }
    expected_status = 204
    patch_request(endpoint, payload, expected_status)


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_using_external_car_type():
    """Patch Apply Settings Using ExternalCarType"""
    endpoint = "/api/v1/applySettings"
    payload = {
        "externalCarType": "P80",
        "patch": {
            "ACTIVE_TIME_MCU": 100,
            "ALTERNATOR_VOLTAGE_TH": 1000,
            "ON_DEMAND_SCAN": 0,
        },
    }
    expected_status = 400
    output = patch_request(endpoint, payload, expected_status)
    error_msg = output["msg"]
    assert error_msg == "Requires { facility } if providing { external_car_type }"


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_using_all_required_fields():
    """Patch Apply Settings Using All Required Fields"""
    deviceID1 = os.environ.get("deviceID1")
    endpoint = "/api/v1/applySettings"
    payload = {
        "facility": "PABTN",
        "externalCarType": "P80",
        "tapeIds": [deviceID1],
        "patch": {
            "ACTIVE_TIME_MCU": 100,
            "ALTERNATOR_VOLTAGE_TH": 1000,
            "ON_DEMAND_SCAN": 0,
        },
    }
    expected_status = 400
    output = patch_request(endpoint, payload, expected_status)
    error_msg = output["msg"]
    assert (
        error_msg
        == "Please provide either: { facility, externalCarType } or { tapeIds }, but not both."
    )


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_without_tapeids():
    """Patch Apply Settings Without tape_ids"""
    endpoint = "/api/v1/applySettings"
    payload = {
        "facility": "PABTN",
        "externalCarType": "P80",
        "patch": {
            "ACTIVE_TIME_MCU": 400,
            "ALTERNATOR_VOLTAGE_TH": 900,
            "ON_DEMAND_SCAN": 0,
        },
    }
    expected_status = 204
    patch_request(endpoint, payload, expected_status)


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_facilty_external_cartype_all_patches():
    """Patch Apply Settings Facility External CarTYpe All Patches"""
    endpoint = "/api/v1/applySettings"
    json_file_path = "data/facility_external_cartype_all_patches.json"
    with open(json_file_path, "r", encoding="ascii") as j:
        contents = json.loads(j.read())
    payload = contents
    expected_status = 204
    patch_request(endpoint, payload, expected_status)


@pytest.mark.regression
@pytest.mark.package_car_settings
@pytest.mark.skip("See bug: SPSF-426")
def test_apply_settings_over_100_tapeids_all_patches():
    """Patch Apply Settings Over 100 Tapeids All Patches"""
    endpoint = "/api/v1/applySettings"
    json_file_path = "data/tapeids_all_patches.json"
    with open(json_file_path, "r", encoding="ascii") as j:
        contents = json.loads(j.read())
    payload = contents
    expected_status = 204
    patch_request(endpoint, payload, expected_status)


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_single_tapeid_all_patches():
    """Patch Apply Settings Single Tapeid All Patches"""
    endpoint = "/api/v1/applySettings"
    json_file_path = "data/single_tapeid_all_patches.json"
    with open(json_file_path, "r", encoding="ascii") as j:
        contents = json.loads(j.read())
    payload = contents
    expected_status = 204
    patch_request(endpoint, payload, expected_status)


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_missing_required_params():
    """Patch Apply Settings Missing Required Params"""
    endpoint = "/api/v1/applySettings"
    payload = {
        "patch": {
            "ACTIVE_TIME_MCU": 400,
            "ALTERNATOR_VOLTAGE_TH": 2000,
            "ON_DEMAND_SCAN": 0,
        }
    }
    expected_status = 400
    output = patch_request(endpoint, payload, expected_status)
    error_msg = output["msg"]
    assert (
        error_msg
        == "Please provide either: { facility, externalCarType } or { tapeIds }, but not both."
    )


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_with_empty_payload():
    """Patch Apply Settings with Empty Payload"""
    endpoint = "/api/v1/applySettings"
    payload = {}
    expected_status = 400
    output = patch_request(endpoint, payload, expected_status)
    error_msg = output["msg"]
    assert error_msg == "Invalid request body."


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_with_missing_patch_values():
    """Patch Apply Settings with missing patch values"""
    deviceID1 = os.environ.get("deviceID1")
    endpoint = "/api/v1/applySettings"
    payload = {"tape_ids": [deviceID1], "patch": {}}
    expected_status = 400
    output = patch_request(endpoint, payload, expected_status)
    error_msg = output["msg"]
    assert error_msg == "Error: Missing field.Please provide: { patch: values }"


### Apply Settings External
@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_external():
    """Patch Apply Settings External"""
    car1 = os.environ.get("car1")
    endpoint = "/ext/api/v1/applySettingsExternal"
    payload = {
        "correlationId": "191919192",
        "deviceIds": [car1],
        "patch": {
            "ON_DEMAND_SCAN": 1,
            "ON_DEMAND_SCAN_DUR_SEC": 86400,
            "UPLOAD_LOG_MIN": 43200,
            "SYSTEM_RESET_FLAG": 1,
            "SELF_TEST": 255,
        },
    }
    expected_status = 204
    patch_request(endpoint, payload, expected_status)


@pytest.mark.regression
@pytest.mark.package_car_settings
@pytest.mark.skip("Related to bug: SPSF-426")
def test_apply_settings_external_with_over_100_devices():
    """Patch Apply Settings External With Over 100 devices"""
    endpoint = "/ext/api/v1/applySettingsExternal"
    json_file_path = "data/external_settings_over_100_devices.json"
    with open(json_file_path, "r", encoding="ascii") as j:
        contents = json.loads(j.read())
    payload = contents
    expected_status = 204
    patch_request(endpoint, payload, expected_status)


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_external_missing_correlationid():
    """Patch Apply Settings External Missing correlationId"""
    car1 = os.environ.get("car1")
    endpoint = "/ext/api/v1/applySettingsExternal"
    payload = {"deviceIds": [car1], "patch": {"ON_DEMAND_SCAN": 0}}
    expected_status = 400
    patch_request(endpoint, payload, expected_status)


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_external_missing_deviceids():
    """Patch Apply Settings External Missing deviceIds"""
    endpoint = "/ext/api/v1/applySettingsExternal"
    payload = {"correlationId": "191919192", "patch": {"ON_DEMAND_SCAN": 0}}
    expected_status = 400
    patch_request(endpoint, payload, expected_status)


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_external_with_rational_num_on_demand_scan():
    """Patch Apply Settings External Rational Number for ON_DEMAND_SCAN"""
    car1 = os.environ.get("car1")
    endpoint = "/ext/api/v1/applySettingsExternal"
    payload = {
        "correlationId": "191919192",
        "deviceIds": [car1],
        "patch": {"ON_DEMAND_SCAN": 1.5},
    }
    expected_status = 400
    patch_request(endpoint, payload, expected_status)


@pytest.mark.regression
@pytest.mark.package_car_settings
def test_apply_settings_external_with_empty_payload():
    """Patch Apply Settings External With Empty Payload"""
    endpoint = "/ext/api/v1/applySettingsExternal"
    payload = {}
    expected_status = 400
    patch_request(endpoint, payload, expected_status)


@pytest.mark.regression
@pytest.mark.package_car_settings
@pytest.mark.end_to_end
def test_end_to_end_apply_internal_settings():
    """End-to-End Apply Internal Settings"""
    deviceID1 = os.environ.get("deviceID1")
    deviceID2 = os.environ.get("deviceID2")
    ### Step1: Get Package Car Settings
    deviceIDs = [
        deviceID1,
        deviceID2,
    ]
    for deviceID in deviceIDs:
        ### Step1: Patch Apply Settings Using tapeIds
        endpoint = "/api/v1/applySettings"
        payload = {
            "tapeIds": [deviceID],
            "patch": {
                "ACTIVE_TIME_MCU": 300,
                "ALTERNATOR_VOLTAGE_TH": 400,
                "ON_DEMAND_SCAN": 0,
            },
        }
        expected_status = 204
        patch_request(endpoint, payload, expected_status)

        ### Step2: Get Package Car Settings Diff
        output = get_request("/pkgCarSettingsDiff?id=" + deviceID, 200)
        pkgCarID = output[0]["pkgCarId"]
        ackUuID = output[0]["ackUuid"]
        update_settings = output[0]["settings"]
        actual_ACTIVE_TIME_MCU = output[0]["settings"]["ACTIVE_TIME_MCU"]
        actual_ALTERNATOR_VOLTAGE_TH = output[0]["settings"]["ALTERNATOR_VOLTAGE_TH"]
        actual_ON_DEMAND_SCAN = output[0]["settings"]["ON_DEMAND_SCAN"]
        print(f"Got ackUuID for Package Car Settings Diff: {ackUuID}")
        print(f"Got total settings: {len(update_settings)}")
        assert pkgCarID == deviceID, "Wrong expected pkCarID found!"
        assert actual_ACTIVE_TIME_MCU == 300, "Wrong expected ACTIVE_TIME_MCU found!"
        assert (
            actual_ALTERNATOR_VOLTAGE_TH == 400
        ), "Wrong expected ALTERNATOR_VOLTATE_TH found!"
        assert actual_ON_DEMAND_SCAN == 0, "Wrong expected ON_DEMAND_SCAN found!"
        assert (
            len(update_settings) == 7
        ), "Wrong expected length of setting object found!"

        ### Step3: Get Package Car Ack
        payload = {"ackUuid": ackUuID}
        post_request2("/pkgCarSettingsAck", payload, expected_status=200)

        ### Step4: Get Package Car Settings Diff and verify settings object is empty
        output = get_request("/pkgCarSettingsDiff?id=" + deviceID, 200)
        pkgCarID = output[0]["pkgCarId"]
        settings_diff = output[0]["settings"]
        assert pkgCarID == deviceID, "Wrong expected pkgCarID found!"
        assert len(settings_diff) == 0, "Expected settings value to be empty hash!"

        ### Step5: Get Settings
        output = get_request("/pkgCarSettings?id=" + deviceID, 200)
        pkgCarID = output[0]["pkgCarId"]
        ackUuID = output[0]["ackUuid"]
        activeTimeMCU = output[0]["settings"]["ACTIVE_TIME_MCU"]
        alternatorVoltageTH = output[0]["settings"]["ALTERNATOR_VOLTAGE_TH"]
        onDemandSCAN = output[0]["settings"]["ON_DEMAND_SCAN"]
        assert pkgCarID == deviceID, "Wrong expected pkgCarID found!"
        print(f"Got current ackUuID: {ackUuID}")
        print(f"Got ACTIVE_TIME_MCU: {activeTimeMCU}")
        print(f"Got ALTERNATOR_VOLTAGE_TH: {alternatorVoltageTH}")
        print(f"Got ON_DEMAND_SCAN: {onDemandSCAN}")


@pytest.mark.regression
@pytest.mark.package_car_settings
@pytest.mark.end_to_end
def test_end_to_end_apply_external_settings_single_device():
    """End-to-End Apply External Settings Single Device"""
    ### Step1: Patch Apply External Settings
    deviceID1 = os.environ.get("deviceID1")
    car1 = os.environ.get("car1")
    endpoint = "/ext/api/v1/applySettingsExternal"
    payload = {
        "correlationId": "191919193",
        "deviceIds": [car1],
        "patch": {
            "ON_DEMAND_SCAN": 1,
            "ON_DEMAND_SCAN_DUR_SEC": 43200,
            "UPLOAD_LOG_MIN": 100,
            "SYSTEM_RESET_FLAG": 0,
            "SELF_TEST": 0,
        },
    }
    expected_status = 204
    patch_request(endpoint, payload, expected_status)

    ### Step2: Get Package Car Settings Diff
    output = get_request("/pkgCarSettingsDiff?id=" + deviceID1, 200)
    pkgCarID = output[0]["pkgCarId"]
    ackUuID = output[0]["ackUuid"]
    assert pkgCarID == deviceID1, "Wrong expected pkgCarID!"
    print(f"Got EXPECTED ackUuID from Package Car Settings Diff: {ackUuID}")

    ### Step3: Get Package Car Ack
    payload = {"ackUuid": ackUuID}
    post_request2("/pkgCarSettingsAck", payload, expected_status=200)

    ### Step4: Get Package Car Settings Diff and verify settings object is empty
    output = get_request("/pkgCarSettingsDiff?id=" + deviceID1, 200)
    pkgCarID = output[0]["pkgCarId"]
    settings_diff = output[0]["settings"]
    assert pkgCarID == deviceID1, "Wrong pkgCarID found!"
    assert len(settings_diff) == 0, "Expected settings value to be empty hash!"

    ### Step5: Get Settings
    output = get_request("/pkgCarSettings?id=" + deviceID1, 200)
    pkgCarID = output[0]["pkgCarId"]
    ackUuID = output[0]["ackUuid"]
    activeTimeMCU = output[0]["settings"]["ACTIVE_TIME_MCU"]
    alternatorVoltageTH = output[0]["settings"]["ALTERNATOR_VOLTAGE_TH"]
    onDemandSCAN = output[0]["settings"]["ON_DEMAND_SCAN"]
    assert pkgCarID == deviceID1, "Wrong pkgCarID found!"
    print(f"Got current ackUuID: {ackUuID}")
    print(f"Got ACTIVE_TIME_MCU: {activeTimeMCU}")
    print(f"Got ALTERNATOR_VOLTAGE_TH: {alternatorVoltageTH}")
    print(f"Got ON_DEMAND_SCAN: {onDemandSCAN}")


@pytest.mark.regression
@pytest.mark.package_car_settings
@pytest.mark.end_to_end
def test_end_to_end_apply_external_settings_multiple_devices():
    """End-to-End Apply External Settings Multiple Devices"""
    ### Step1: Patch Apply External Settings
    car1 = os.environ.get("car1")
    car2 = os.environ.get("car2")
    endpoint = "/ext/api/v1/applySettingsExternal"
    payload = {
        "correlationId": "191919194",
        "deviceIds": [car1, car2],
        "patch": {
            "ON_DEMAND_SCAN": 1,
            "ON_DEMAND_SCAN_DUR_SEC": 43200,
            "UPLOAD_LOG_MIN": 100,
            "SYSTEM_RESET_FLAG": 0,
            "SELF_TEST": 0,
        },
    }
    expected_status = 204
    patch_request(endpoint, payload, expected_status)

    ### Step2: Get Package Car Settings Diff
    deviceID1 = os.environ.get("deviceID1")
    deviceID2 = os.environ.get("deviceID2")
    device_list = [deviceID1, deviceID2]

    for deviceID in device_list:
        ### Step2: Get Package Car Settings Diff
        output = get_request("/pkgCarSettingsDiff?id=" + deviceID, 200)
        pkgCarID = output[0]["pkgCarId"]
        ackUuID = output[0]["ackUuid"]
        assert pkgCarID == deviceID
        print(f"Got EXPECTED ackUuID from Package Car Settings Diff: {ackUuID}")

        ### Step3: Get Package Car Ack
        payload = {"ackUuid": ackUuID}
        post_request2("/pkgCarSettingsAck", payload, expected_status=200)

        ### Step4: Get Package Car Settings Diff
        output = get_request("/pkgCarSettingsDiff?id=" + deviceID, 200)
        pkgCarID = output[0]["pkgCarId"]
        settings_diff = output[0]["settings"]
        assert pkgCarID == deviceID
        assert settings_diff == {}, "Expected settings value to be empty hash!"

        ### Step5: Get Settings
        output = get_request("/pkgCarSettings?id=" + deviceID, 200)
        pkgCarID = output[0]["pkgCarId"]
        ackUuID = output[0]["ackUuid"]
        activeTimeMCU = output[0]["settings"]["ACTIVE_TIME_MCU"]
        alternatorVoltageTH = output[0]["settings"]["ALTERNATOR_VOLTAGE_TH"]
        onDemandSCAN = output[0]["settings"]["ON_DEMAND_SCAN"]
        assert pkgCarID == deviceID
        print(f"Got current ackUuID: {ackUuID}")
        print(f"Got ACTIVE_TIME_MCU: {activeTimeMCU}")
        print(f"Got ALTERNATOR_VOLTAGE_TH: {alternatorVoltageTH}")
        print(f"Got ON_DEMAND_SCAN: {onDemandSCAN}")
