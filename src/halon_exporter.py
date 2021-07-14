#!/usr/bin/env python3

from halon_api import HalonAPI
from prometheus_client import start_http_server, Info, Gauge, Enum
from requests import ConnectionError, HTTPError

import os
import time

# Mandatory env variables
halon_user = os.environ["HALON_USER"]
halon_password = os.environ["HALON_PASSWORD"]
halon_host = os.environ["HALON_HOST"]

# Check certs by default
halon_verify = os.environ.get("HALON_VERIFY", "true")

# Default port exporter will listen on
halon_exporter_port = os.environ.get("HALON_EXPORTER_PORT", 9838)

# Converts HALON_VERIFY to Bool if false/true
if halon_verify.lower() == "false":
    halon_verify = False
elif halon_verify.lower() == "true":
    halon_verify = True

# The Halon API
h = HalonAPI(halon_host, halon_user, halon_password, verify=halon_verify)

# This MUST be first declared metric. The other metrics are gathered as a
# side effect of this metric's set function.
FAILED_API_REQUESTS = Gauge(
    "halon_http_errors",
    "The number of request to the Halon API that returned an HTTP error code",
)
FAILED_API_REQUESTS.set_function(lambda: get_metrics())

UP = Gauge("halon_up", "Halon is up")

CONFIG_REVISIONS = Gauge("halon_config_revisions", "Number of config revisions")

SYSTEM_UPTIME = Gauge("halon_system_uptime_seconds", "Seconds since the system started")

LICENSE_STATUS = Enum(
    "halon_license_status",
    "Status of the Halon license",
    states=["idle", "refreshing", "ok", "error"],
)

INFO = Info("halon", "Halon info")

SYSTEM_NEWER_VERSIONS = Gauge(
    "halon_system_newer_versions",
    "Number of newer Halon versions available",
)

STAT = Gauge(
    "halon_statistic",
    "Halon statistic",
    ["namespace", "name", "legend"],
)


def count_errors(func):
    """Counting HTTPErrors in decorated function"""

    def wrapper():
        try:
            # This is the request to the Halon API
            func()
            return 0  # No error occured
        except HTTPError:
            return 1  # An error occured

    return wrapper


@count_errors
def get_config_revisions():
    """Get the number of config revisions"""
    CONFIG_REVISIONS.set(len(h.list_config_revisions(limit=2000)))


@count_errors
def get_license_status():
    '''Asuming license is OK unless status is "error".
    Possible states are: "idle" "refreshing" "ok" "error"'''
    LICENSE_STATUS.state(h.get_license()["status"])
    # status = h.get_license()["status"]
    # LICENSE_STATUS.labels(status).set(int(status != "error"))


@count_errors
def get_system_uptime():
    """Get the system uptime"""
    SYSTEM_UPTIME.set(h.get_system_uptime())


@count_errors
def get_stats():
    """Get all statistics data"""
    for d in h.list_stats(limit=1000):
        STAT.labels(d["namespace"], d["name"], d["legend"]).set(d["count"])


@count_errors
def get_info():
    """Info as labels"""
    d = {
        "version": h.get_software_version(),
        "time": h.get_system_time(),
    }
    INFO.info(d)


@count_errors
def get_system_newer_versions():
    available_versions = set(v["version"] for v in h.get_latest_software_version())
    current_version = set([h.get_software_version()])
    newer_versions = available_versions - current_version
    SYSTEM_NEWER_VERSIONS.set(len(newer_versions))


def get_metrics():
    """Get the metrics. Report HTTP errors"""
    try:
        # Count HTTP errors
        e = 0
        e += get_system_uptime()
        e += get_config_revisions()
        e += get_system_newer_versions()
        e += get_license_status()
        e += get_stats()
        e += get_info()

        # Halon is up
        UP.set(1)

        # The number of HTTP errors
        return e

    except (ConnectionError):
        # Halon is down
        UP.set(0)


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(int(halon_exporter_port))

    # Wait for requests
    while True:
        time.sleep(30.0)
