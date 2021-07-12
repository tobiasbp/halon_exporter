# halon_exporter
A prometheus exporter for the mail transport agent (MTA) [Halon](https://halon.io/).
Built with [Promethus Python Client](https://github.com/prometheus/client_python).
Exposed metrics are collected using the [Halon API](https://docs.halon.io/api/) using the
PyPI package [halon-api](https://pypi.org/project/halon-api/).

# How to use
Set the following environment variables:
* `export HALON_USER='halon-user'`
* `export HALON_PASSWORD='secret-password'`
* `export HALON_HOST='halon.example.org'`

Run the exporter: `./halon_exporter`
Access metrics at `http://localhost:8000`

# Metrics
The metrics exported.

## Halon
Metrics from halon.
* `halon_statistic{legend="*",name="*",namespace="*"} VALUE`
* `halon_system_newer_versions VALUE`
* `halon_info{time="*",version="*"} 1.0`
* `halon_license_status{halon_license_status="idle"} VALUE`
* `halon_license_status{halon_license_status="refreshing"} VALUE`
* `halon_license_status{halon_license_status="ok"} VALUE`
* `halon_license_status{halon_license_status="error"} VALUE`
* `halon_system_uptime_seconds VALUE`
* `halon_config_revisions VALUE`
* `halon_up [0.0|1.0]`
* `halon_http_errors VALUE`
## System
Metrics from the exporter.
* `?`
* `?`
