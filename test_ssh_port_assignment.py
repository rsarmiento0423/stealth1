""" SSH Port Assignment Tests """

import os
import time
import requests
import pytest
from utils.libs import get_request, generate_macid, is_valid_time_format


### Request-Port API tests
@pytest.mark.regression
@pytest.mark.ssh_port_assignment
def test_get_request_port_for_1min():
    """Get Request Port set for 1 min"""
    macID = generate_macid()
    output = get_request("/request-port?macid=" + macID + "&minutes=1", 200)
    print(f"JSON output:{output}")
    assert output["macId"] == macID
    port_num = str(output["port"])
    assert len(port_num) == 5
    assert output["minutes"] == 1
    assert is_valid_time_format(output["cutoff_time"]), "Wrong format for 'cutoff_time'"


@pytest.mark.maxoutports
def test_get_request_maxports():
    """Get Request Port for max ports"""
    for i in range(5):
        macID = generate_macid()
        output = get_request("/request-port?macid=" + macID + "&minutes=1", 200)
        print(f"JSON output:{output}")
        assert output["macId"] == macID
        port_num = str(output["port"])
        assert len(port_num) == 5
        assert output["minutes"] == 1
        assert is_valid_time_format(
            output["cutoff_time"]
        ), "Wrong format for 'cutoff_time'"
        print(f"Iteration: {i}")

        time.sleep(0.5)
        with open("ssh-ports.txt", "a", encoding="ascii") as f:
            f.write(f"{port_num}" + "\n")


@pytest.mark.regression
@pytest.mark.ssh_port_assignment
def test_get_request_port_set_default():
    """Get Request Port with 30 min default"""
    macID = generate_macid()
    output = get_request("/request-port?macid=" + macID, 200)
    print(f"JSON output:{output}")
    assert output["macId"] == macID
    port_num = str(output["port"])
    assert len(port_num) == 5
    assert output["minutes"] == 30
    assert is_valid_time_format(output["cutoff_time"]), "Wrong format for 'cutoff_time'"


@pytest.mark.regression
@pytest.mark.ssh_port_assignment
def test_get_request_port_set_1440min():
    """Get Request Port set to 1440 min"""
    macID = generate_macid()
    output = get_request("/request-port?macid=" + macID + "&minutes=1440", 200)
    assert output["macId"] == macID
    port_num = str(output["port"])
    assert len(port_num) == 5
    assert output["minutes"] == 1440
    assert is_valid_time_format(output["cutoff_time"]), "Wrong format for 'cutoff_time'"


@pytest.mark.regression
@pytest.mark.ssh_port_assignment
def test_get_request_port_mixed_value_minutes():
    """Get Request Port set to mixed minutes value"""
    macID = generate_macid()
    expected_status = 400
    endpoint = "/request-port?macid=" + macID + "&minutes=3a"
    resp = requests.get(os.environ.get("HOST") + endpoint, timeout=2)
    status_code = resp.status_code
    print(f"Status Code: {status_code}")
    assert status_code == expected_status
    expected_error = "The 'minutes' parameter is invalid OR exceeds 24 hours"
    print(f"Got actual error: {resp.text}")
    assert expected_error == resp.text


### Add-Port-Time API tests
@pytest.mark.regression
@pytest.mark.ssh_port_assignment
def test_get_add_port_set_1min():
    """Get Add Port Time Set to 1 min"""
    macID = generate_macid()
    output = get_request("/request-port?macid=" + macID + "&minutes=1", 200)
    print(f"JSON output:{output}")
    assert output["macId"] == macID
    port_num1 = str(output["port"])
    assert len(port_num1) == 5
    assert output["minutes"] == 1
    assert is_valid_time_format(output["cutoff_time"]), "Wrong format for 'cutoff_time'"

    output = get_request("/add-port-time?macid=" + macID + "&minutes=1", 200)
    print(f"JSON output:{output}")
    assert output["macid"] == macID
    port_num2 = str(output["port"])
    assert port_num1 == port_num2
    assert is_valid_time_format(output["cutoff_time"]), "Wrong format for 'cutoff_time'"


@pytest.mark.regression
@pytest.mark.ssh_port_assignment
def test_get_add_port_time_set_0min():
    """Get Add Port Time Set to 0 min"""
    macID = generate_macid()
    output = get_request("/request-port?macid=" + macID + "&minutes=1", 200)
    print(f"JSON output:{output}")
    assert output["macId"] == macID
    port_num1 = str(output["port"])
    assert len(port_num1) == 5
    assert output["minutes"] == 1
    assert is_valid_time_format(output["cutoff_time"]), "Wrong format for 'cutoff_time'"

    expected_status = 400
    endpoint = "/add-port-time?macid=" + macID + "&minutes=0"
    resp = requests.get(os.environ.get("HOST") + endpoint, timeout=2)
    status_code = resp.status_code
    print(f"Status Code: {status_code}")
    assert status_code == expected_status
    expected_error = "Invalid parameter 'minutes'"
    print(f"Got actual error: {resp.text}")
    assert expected_error == resp.text


@pytest.mark.regression
@pytest.mark.ssh_port_assignment
def test_get_add_port_time_mixed_value_minutes():
    """Get Add Port Time set to mixed value minutes"""
    macID = generate_macid()
    output = get_request("/request-port?macid=" + macID + "&minutes=1", 200)
    print(f"JSON output:{output}")
    assert output["macId"] == macID
    port_num1 = str(output["port"])
    assert len(port_num1) == 5
    assert output["minutes"] == 1
    assert is_valid_time_format(output["cutoff_time"]), "Wrong format for 'cutoff_time'"

    expected_status = 400
    endpoint = "/add-port-time?macid=" + macID + "&minutes=3a"
    resp = requests.get(os.environ.get("HOST") + endpoint, timeout=2)
    status_code = resp.status_code
    print(f"Status Code: {status_code}")
    assert status_code == expected_status
    expected_error = "Invalid parameter 'minutes'"
    print(f"Got actual error: {resp.text}")
    assert expected_error == resp.text


### Lookup-Port API tests
@pytest.mark.regression
@pytest.mark.ssh_port_assignment
def test_get_lookup_port_number():
    """Get Lookup Port Number after successful request-port"""
    macID = generate_macid()
    output = get_request("/request-port?macid=" + macID + "&minutes=1", 200)
    print(f"JSON output:{output}")
    assert output["macId"] == macID
    port_num1 = output["port"]
    assert output["minutes"] == 1
    assert is_valid_time_format(output["cutoff_time"]), "Wrong format for 'cutoff_time'"

    port_num2 = get_request("/lookup-port?macid=" + macID, 200)
    print(f"Got port number: {port_num2}")
    assert port_num1 == port_num2


@pytest.mark.regression
@pytest.mark.ssh_port_assignment
def test_get_zero_lookup_port_number():
    """Get Zero Lookup Port Number after minutes limit reached"""
    macID = generate_macid()
    output = get_request("/request-port?macid=" + macID + "&minutes=1", 200)
    print(f"JSON output:{output}")
    assert output["macId"] == macID
    port_num1 = str(output["port"])
    assert len(port_num1) == 5
    assert output["minutes"] == 1
    assert is_valid_time_format(output["cutoff_time"]), "Wrong format for 'cutoff_time'"

    time.sleep(90)
    port_num2 = get_request("/lookup-port?macid=" + macID, 200)
    print(f"Got port number: {port_num2}")
    assert int(port_num1) != int(port_num2)


@pytest.mark.regression
@pytest.mark.ssh_port_assignment
def test_missing_macid_lookup_port_number():
    """Get Lookup Port with missing macid"""
    expected_status = 400
    endpoint = "/lookup-port?macid="
    resp = requests.get(os.environ.get("HOST") + endpoint, timeout=2)
    status_code = resp.status_code
    print(f"Status Code: {status_code}")
    assert status_code == expected_status
    expected_error = "Invalid macId."
    print(f"Got actual error: {resp.text}")
    assert expected_error == resp.text


@pytest.mark.regression
@pytest.mark.ssh_port_assignment
def test_non_existing_macid():
    """Get Lookup Port with non-existing macid"""
    port_num = get_request("/lookup-port?macid=3a", 200)
    print(f"Got port number: {port_num}")
    assert int(port_num) == 0
