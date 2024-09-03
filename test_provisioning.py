""" Package Car Settings Tests """

import os
import pytest
from utils.libs import post_request3, put_request2


### Provisioning
@pytest.mark.skip("Skip test")
@pytest.mark.provisioning
def test_add_update_tape_():
    """Add/Update tape"""
    deviceID1 = os.environ.get("deviceID1")
    car1 = os.environ.get("car1")
    qr_code1 = os.environ.get("qr_code1")

    ### Add tape
    facility = "TEST"
    payload = {}
    output = post_request3(
        "/associations/addtape?facility=" + facility, payload, expected_status=200
    )
    data_id = output["data"]
    print(f"Got id: {data_id}")

    ### Update tape
    payload = {
        "facility": facility,
        "AssetBarcode": car1,
        "tape_id": deviceID1,
        "qrcode": qr_code1,
        "action": 0,
        "id": "26116",
    }

    print(f"Payload type: {type(payload)}")
    print(f"id: {payload['id']}")
    payload["id"] = data_id
    print(f"Updated payload: {payload}")

    output = put_request2("/associations/updatetape", payload, expected_status=200)
    msg = output["msg"]
    print(f"Got message: {msg}")
    expected_msg = "Record updated!"
    assert msg == expected_msg, f"Wrong message displayed. Expected: {expected_msg}!"


@pytest.mark.provisioning
def test_e2e_provisioning():
    """test_e2e_provisioning"""
    deviceID1 = os.environ.get("deviceID1")
    car1 = os.environ.get("car1")
    qr_code1 = os.environ.get("qr_code1")

    ### Add tape
    facility = "TEST"
    payload = {}
    output = post_request3(
        "/associations/addtape?facility=" + facility, payload, expected_status=200
    )
    data_id = output["data"]
    print(f"Got id: {data_id}")

    ### Update tape
    payload = {
        "facility": facility,
        "AssetBarcode": car1,
        "tape_id": deviceID1,
        "qrcode": qr_code1,
        "id": "26116",
    }

    print(f"Payload type: {type(payload)}")
    print(f"id: {payload['id']}")
    payload["id"] = data_id  # Update id
    print(f"Updated payload: {payload}")

    output = put_request2("/associations/updatetape", payload, expected_status=200)
    msg = output["msg"]
    print(f"Got message: {msg}")
    expected_msg = "Record updated!"
    assert msg == expected_msg, f"Wrong message displayed. Expected: {expected_msg}!"

    ### Replace
    deviceID2 = os.environ.get("deviceID2")
    qr_code2 = os.environ.get("qr_code2")
    car1 = os.environ.get("car1")

    payload = {
        "AssertBarCode": car1,
        "tape_id": deviceID2,
        "qrcode": qr_code2,
        "id": data_id,
    }
    output = put_request2("/associations/updatetape", payload, expected_status=200)
    msg = output["msg"]
    print(f"Got message: {msg}")
    expected_msg = "Record updated!"
    assert msg == expected_msg, f"Wrong message displayed. Expected: {expected_msg}!"

    ### Reassign
    car1 = os.environ.get("car1")
    payload = {"AssetBarcode": car1, "id": data_id}
    output = put_request2("/associations/updatetape", payload, expected_status=200)
    msg = output["msg"]
    print(f"Got message: {msg}")
    expected_msg = "Vehicle has already been associated."
    assert msg == expected_msg, f"Wrong message displayed. Expected: {expected_msg}!"
