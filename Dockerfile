FROM alpine:latest
LABEL authors="Cyantize"


# Install Python3 and pip
RUN apk add --no-cache python3 py3-pip py3-virtualenv libmagic

WORKDIR /usr/src/app

# Copy the project files to the container
COPY . .

RUN python3 -m virtualenv /usr/src/venv && /usr/src/venv/bin/pip install .
RUN rm -rf /usr/src/app

# Command to run the Python package when the container starts
CMD ["/usr/src/venv/bin/python3", "-m", "cyantize"]
