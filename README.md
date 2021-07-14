# halon_exporter
A [prometheus](https://prometheus.io/) exporter for the mail transport agent (MTA) [Halon](https://halon.io/).
Built with [Promethus Python Client](https://github.com/prometheus/client_python).
Exposed metrics are collected using the [Halon API](https://docs.halon.io/api/) using the
PyPI package [halon-api](https://pypi.org/project/halon-api/).

# Configuration

Set the following environment variables:
* `export HALON_USER='halon-user'`
* `export HALON_PASSWORD='secret-password'`
* `export HALON_HOST='halon.example.org'`

Optionally, if you use your own CA, set `HALON_VERIFY` to the path to your CA_BUNDLE:
* `export HALON_VERIFY='/my/ca_bundle.pem'`

If you do not want to verify the certificate on the Halon server, you can
set `HALON_VERIFY` to `False`.

The default port for the exporter is 9838. You can set at different
port with the environment variable `HALON_EXPORTER_PORT`.

# Running directly
Run the exporter: `./halon_exporter.py`
Then access the Halon metrics at `http://localhost:9838`

# Running in Docker

* Pull the image: `docker pull tobiasbp/halon-exporter:latest`
* Run a container: `docker run --rm --env HALON_HOST=halon.example.org --env HALON_USER=halon-user --env HALON_PASSWORD=secret-password -p 9838:9838 tobiasbp/halon-exporter`
* Access metrics at: `http://localhost:9838`

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
