FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y gcc g++ pkg-config libhdf5-dev git && \
    rm -rf /var/lib/apt/lists/*

RUN apt update && \
    apt install curl

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt