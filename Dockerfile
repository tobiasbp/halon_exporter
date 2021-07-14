FROM python:3.9-alpine

# Expose port
EXPOSE 9838

# Install python packages
COPY requirements.txt .
RUN pip install --requirement requirements.txt

# Add the exporter
COPY src/halon_exporter.py /usr/local/bin/

# Run as non-privileged user
USER nobody

# Run the exporter
ENTRYPOINT [ "python", "/usr/local/bin/halon_exporter.py" ]
