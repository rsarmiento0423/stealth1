""" Flow 1 Tests """

import pytest
from utils.libs import get_request, post_request, put_request


### Get Settings API test
@pytest.mark.regression
@pytest.mark.flow1
def test_get_settings():
    """Get Settings"""
    output = get_request("/gwSettings?cartype=P10&facility=PABTN", 200)
    carType = output["carType"]
    assert carType == "P10"


### Insert Settings API tests
@pytest.mark.regression
@pytest.mark.flow1
def test_insert_new_settings():
    """Insert Settings with valid JSON payload"""
    endpoint = "/gwSettings"
    json_file_path = "data/insert_p10.json"
    expected_status = 200
    output = post_request(endpoint, json_file_path, expected_status)
    msg = output["msg"]
    assert msg == "Item already exists for Facility: PABTN || carType: P10"


@pytest.mark.regression
@pytest.mark.flow1
def test_insert_missing_cartype():
    """Insert Settings with missing 'carType in JSON payload"""
    endpoint = "/gwSettings"
    json_file_path = "data/insert_missing_cartype.json"
    expected_status = 400
    output = post_request(endpoint, json_file_path, expected_status)
    msg = output["details"]
    assert msg == [{"field": "carType", "message": "Required"}]


@pytest.mark.flow1
@pytest.mark.skip(reason="See Bug: SPSF-319")
def test_insert_empty_facility():
    """Insert Settings with empty string value for 'Facility' in JSON payload"""
    endpoint = "/gwSettings"
    json_file_path = "data/insert_empty_facility.json"
    expected_status = 400
    post_request(endpoint, json_file_path, expected_status)


@pytest.mark.regression
@pytest.mark.flow1
def test_insert_missing_facility():
    """Insert Settings without 'Facility' in JSON payload"""
    endpoint = "/gwSettings"
    json_file_path = "data/insert_missing_facility.json"
    expected_status = 400
    output = post_request(endpoint, json_file_path, expected_status)
    msg = output["details"]
    assert msg == [{"field": "facility", "message": "Required"}]


@pytest.mark.regression
@pytest.mark.flow1
def test_insert_missing_hwversion():
    """Insert Setting without 'hwversion in JSON payload"""
    endpoint = "/gwSettings"
    json_file_path = "data/insert_missing_hwversion.json"
    expected_status = 400
    output = post_request(endpoint, json_file_path, expected_status)
    msg = output["details"]
    assert msg == [{"field": "hwVersion", "message": "Required"}]


@pytest.mark.regression
@pytest.mark.flow1
def test_insert_missing_pirtype():
    """Insert Setting without 'pirType' in JSON payload"""
    endpoint = "/gwSettings"
    json_file_path = "data/insert_missing_pirtype.json"
    expected_status = 400
    output = post_request(endpoint, json_file_path, expected_status)
    msg = output["details"]
    assert msg == [{"field": "pirType", "message": "Required"}]


@pytest.mark.regression
@pytest.mark.flow1
def test_insert_empty_payload():
    """Insert Setting with empty JSON payload"""
    endpoint = "/gwSettings"
    json_file_path = "data/empty_payload.json"
    expected_status = 400
    output = post_request(endpoint, json_file_path, expected_status)
    msg = output["details"]
    assert msg == [
        {"field": "carType", "message": "Required"},
        {"field": "settings", "message": "Required"},
        {"field": "facility", "message": "Required"},
        {"field": "hwVersion", "message": "Required"},
        {"field": "pirType", "message": "Required"},
    ]


@pytest.mark.flow1
@pytest.mark.skip(reason="See Bug: SPSF-343")
def test_insert_setting_with_empty_string_for_carType():
    """Insert Setting with empty value for carType in payload"""
    endpoint = "/gwSettings"
    json_file_path = "data/empty_cartype.json"
    expected_status = 400
    output = post_request(endpoint, json_file_path, expected_status)
    return output


@pytest.mark.flow1
@pytest.mark.skip(reason="See Bug: SPSF-343")
def test_insert_setting_with_unknown_carType():
    """Insert Setting with unknown carType in payload"""
    endpoint = "/gwSettings"
    json_file_path = "data/unknown_cartype.json"
    expected_status = 400
    output = post_request(endpoint, json_file_path, expected_status)
    return output


### Update Settings API tests
@pytest.mark.regression
@pytest.mark.flow1
def test_update_settings(edit_active_alias):
    """Update Setting with valid JSON payload"""
    endpoint = "/gwSettings"
    json_file_path = "data/update.json"
    expected_status = 200
    output = put_request(endpoint, json_file_path, expected_status)
    carType = output["carType"]
    assert carType == "P10"


@pytest.mark.regression
@pytest.mark.flow1
def test_update_settings_with_empty_payload():
    """Update Setting with empty JSON payload"""
    endpoint = "/gwSettings"
    json_file_path = "data/empty_payload.json"
    expected_status = 400
    output = put_request(endpoint, json_file_path, expected_status)
    msg = output["details"]
    assert msg == [
        {"field": "carType", "message": "Required"},
        {"field": "settings", "message": "Required"},
        {"field": "facility", "message": "Required"},
        {"field": "hwVersion", "message": "Required"},
        {"field": "pirType", "message": "Required"},
    ]
