"""libs.py"""

import os
import json
import random
from datetime import datetime
import requests


def get_request(endpoint, expected_status):
    """get_request"""
    resp = requests.get(os.environ.get("HOST") + endpoint, timeout=2)
    status_code = resp.status_code
    print(f"Status Code: {status_code}")
    assert status_code == expected_status, f"Expected status code: {expected_status}!"
    print(f"Got GET response: {resp.json()}")
    return resp.json()


def post_request(endpoint, json_file_path, expected_status):
    """post_request"""
    with open(json_file_path, "r", encoding="ascii") as j:
        contents = json.loads(j.read())
    payload = contents
    hdrs = {"Content-type": "application/json"}

    resp = requests.post(
        os.environ.get("HOST") + endpoint,
        timeout=2,
        data=json.dumps(payload),
        headers=hdrs,
    )
    status_code = resp.status_code
    print(f"Status Code: {status_code}")
    assert status_code == expected_status, f"Expected status code: {expected_status}!"
    print(f"Got POST response: {resp.json()}")
    return resp.json()


def post_request2(endpoint, contents, expected_status):
    """post_request2"""
    payload = contents
    hdrs = {"Content-type": "application/json"}

    resp = requests.post(
        os.environ.get("HOST") + endpoint,
        timeout=2,
        data=json.dumps(payload),
        headers=hdrs,
    )

    status_code = resp.status_code
    print(f"Status Code: {status_code}")
    assert status_code == expected_status, f"Expected status code: {expected_status}!"
    if status_code == 200:
        return resp
    return resp.json()


def post_request3(endpoint, contents, expected_status):
    """post_request3"""
    payload = contents
    hdrs = {"Content-type": "application/json"}

    resp = requests.post(
        os.environ.get("HOST") + endpoint,
        timeout=2,
        data=json.dumps(payload),
        headers=hdrs,
    )

    status_code = resp.status_code
    print(f"Status Code: {status_code}")
    assert status_code == expected_status, f"Expected status code: {expected_status}!"
    return resp.json()


def put_request(endpoint, json_file_path, expected_status):
    """put_request"""
    with open(json_file_path, "r", encoding="ascii") as j:
        contents = json.loads(j.read())
    payload = contents
    hdrs = {"Content-type": "application/json"}

    resp = requests.put(
        os.environ.get("HOST") + endpoint,
        timeout=2,
        data=json.dumps(payload),
        headers=hdrs,
    )
    status_code = resp.status_code
    print(f"Status Code: {status_code}")
    assert status_code == expected_status, f"Expected status code: {expected_status}!"
    print(f"Got PUT response: {resp.json()}")
    return resp.json()


def put_request2(endpoint, contents, expected_status):
    """put_request2"""
    payload = contents
    hdrs = {"Content-type": "application/json"}

    resp = requests.put(
        os.environ.get("HOST") + endpoint,
        timeout=2,
        data=json.dumps(payload),
        headers=hdrs,
    )

    status_code = resp.status_code
    print(f"Status Code: {status_code}")
    assert status_code == expected_status, f"Expected status code: {expected_status}!"
    if status_code == 200:
        return resp.json()
    return resp.json()


def patch_request(endpoint, contents, expected_status):
    """patch_request"""
    payload = contents
    hdrs = {"Content-type": "application/json"}

    resp = requests.patch(
        os.environ.get("HOST") + endpoint,
        timeout=10,
        data=json.dumps(payload),
        headers=hdrs,
    )
    status_code = resp.status_code
    print(f"Status Code: {status_code}")
    assert status_code == expected_status, f"Expected status code: {expected_status}!"
    if len(resp.text) == 0:
        return resp.text
    print(f"Got PATCH response: {resp.json()}")
    return resp.json()


def generate_macid():
    """generate_macid"""
    number = random.randint(10000, 99999)
    macid = "raytest" + str(number)
    return macid


def is_valid_time_format(time_str):
    """is_valid_time_format"""
    try:
        datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return True
    except ValueError:
        print(f"Got time stamp: {time_str}")
        return False
