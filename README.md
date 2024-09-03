# SPSF QA Test Automation

How to use the SPSF QA Automation Framework

## Description

This project is for running automated API tests on SPSF Core Services to ensure quality is up to company standards.

## Prequisites

* Install Python 3 via https://www.python.org/downloads/

* Create a Python virtual environment: https://www.python.org/downloads/

### Installing

* From the command-line terminal under qa-spsf-core-services directory, enter: ```pip install -r requirements.txt```

### Executing SPSF Smoke tests using `Pytest`

* From command-line terminal, enter: ```pytest -m regression``` to execute all SPSF Regression tests in parallel using 4 workers.

### Executing SPSF Load test using `Locust`

* From the command-line, enter: ```locust`` then point browser to URL: https:\\localhost:8089
From Locust browser page with Start new load test header, enter the following
- Number of users
- Ramp up (users started/second)
- Host: (https://trk-spsf-dev-test.azure-api.net/)
- Advanced options a.k.a. duration: (10m)

### References

* [Python Downloads](https://www.python.org/downloads/)
* [Virtual Environments](https://docs.python.org/3/library/venv.html)
* [Pytest](https://docs.pytest.org/en/stable/index.html)
* [Locust](https://locust.io/)