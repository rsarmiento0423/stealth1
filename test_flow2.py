""" Flow 2 Tests """

import os
import json
import pytest
import requests


### Apply Settings API tests
payloaddata = [
    [{"facility": "PABTN", "carType": "P10"}, 200],
    [{}, 400],
    [{"facility": "PABTN"}, 400],
    [{"carType": "P10"}, 400],
]


@pytest.mark.regression
@pytest.mark.flow2
@pytest.mark.parametrize("payload, http_status_code", payloaddata)
def test_apply_settings(payload, http_status_code):
    """Apply Settings"""
    if http_status_code == 400:
        pytest.skip("See bug: SPSF-320")
    else:
        hdrs = {"Content-Type": "application/json"}
        resp = requests.post(
            os.environ.get("HOST") + "/applyGwSettings",
            timeout=2,
            data=json.dumps(payload),
            headers=hdrs,
        )
        status_code = resp.status_code
        print(
            f"Got Status Code: {status_code}, Expected Status Code: {http_status_code}"
        )
        assert status_code == http_status_code
        print(f"Got response: {resp.text}")
