""" Benchmark Package Car Settings Tests"""

import os
from utils.libs import get_request


def get_package_car_settings():
    """Get Package Car Settings"""
    deviceID1 = os.environ.get("deviceID1")
    output = get_request("/pkgCarSettings?id=" + deviceID1, 200)
    pkgCarID = output[0]["pkgCarId"]
    ackUuID = output[0]["ackUuid"]
    assert pkgCarID == deviceID1
    assert len(ackUuID) == 23


def test_package_car_settings(benchmark):
    benchmark(get_package_car_settings)
