# Container image that runs your code
FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y \
    build-essential \
    python3-pip \
    python3.8

# Copies code file action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

COPY check_basebranch.py /check_basebranch.py

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
