"""Fixtures"""

import os
import random
import json
import pytest


@pytest.fixture(scope="session", autouse=True)
def set_env():
    """Set Environment Variables"""
    with open("config.json", encoding="UTF-8") as f:
        data = json.load(f)
    host = data["HOST"]
    deviceID1 = data["deviceID1"]
    deviceID2 = data["deviceID2"]
    deviceID3 = data["deviceID3"]
    car1 = data["car1"]
    car2 = data["car2"]
    qr_code1 = data["qr_code1"]
    qr_code2 = data["qr_code2"]
    os.environ["HOST"] = host
    os.environ["deviceID1"] = deviceID1
    os.environ["deviceID2"] = deviceID2
    os.environ["deviceID3"] = deviceID3
    os.environ["car1"] = car1
    os.environ["car2"] = car2
    os.environ["qr_code1"] = qr_code1
    os.environ["qr_code2"] = qr_code2


@pytest.fixture()
def edit_active_alias():
    """edit_active_alias"""
    items = [
        ["P100", "P1000", "P100D", "Hello"],
        ["P100D", "Hello", "P100", "P1000"],
        ["P100", "P100D", "Hello", "P1000"],
    ]
    selected_item = random.choice(items)
    json_file_path = "data/update.json"
    with open(json_file_path, "r", encoding="ascii") as j:
        contents = json.loads(j.read())
    data = contents
    print(f"Got old activeAlias: {data['activeAlias']}")
    data["activeAlias"] = selected_item
    print(f"Got new activeAlias: {data['activeAlias']}")
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
