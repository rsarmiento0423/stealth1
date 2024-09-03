""" Flow 3 Tests """

import os
import pytest
from utils.libs import get_request, post_request2, post_request


### Get Settings Diff API test
@pytest.mark.regression
@pytest.mark.flow3
def test_get_settings_diff():
    """Get Settings Diff"""
    deviceID3 = os.environ.get("deviceID3")
    output = get_request("/getSettingsDiff/?id=" + deviceID3, 200)
    assert output[0]["pkgCarId"] == deviceID3
    ackUuid = output[0]["ackUuid"]
    assert len(ackUuid) == 23


### Get Settings Compressed API test
@pytest.mark.regression
@pytest.mark.flow3
def test_get_settings_compressed():
    """Get Settings Compressed"""
    deviceID3 = os.environ.get("deviceID3")
    output = get_request("/getSettingsCompressed/?id=" + deviceID3, 200)
    pkgCarId = output[0]["pkgCarId"]
    ackUuid = output[0]["ackUuid"]
    assert pkgCarId == deviceID3
    assert len(ackUuid) == 23


### Settings Acknowledgement API tests
@pytest.mark.regression
@pytest.mark.flow3
def test_settings_acknowledgement_ackuuid_present():
    """Settings Acknowledgement 'ackUuid' Present"""
    deviceID3 = os.environ.get("deviceID3")
    output = get_request("/getSettingsDiff/?id=" + deviceID3, 200)
    assert output[0]["pkgCarId"] == deviceID3
    ackUuid = output[0]["ackUuid"]
    endpoint = "/settingsAcknowledge"
    json_data = {"ackUuid": ackUuid}
    print(f"Input JSON data: {json_data}")
    expected_status = 200
    post_request2(endpoint, json_data, expected_status)


@pytest.mark.flow3
@pytest.mark.skip(reason="See Bug: SPSF-316")
def test_settings_acknowledgement_ackuuid_not_present():
    """Settings Acknowledgement 'ackUuid' Not Present"""
    endpoint = "/settingsAcknowledge"
    json_file_path = "data/settings_acknowledgement_ackuuid_not_present.json"
    expected_status = 400
    post_request(endpoint, json_file_path, expected_status)
