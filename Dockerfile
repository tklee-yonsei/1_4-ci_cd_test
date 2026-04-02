FROM python:3.10-slim

# 시스템 패키지
RUN apt-get update && \
    apt-get install -y gcc g++ pkg-config libhdf5-dev && \
    rm -rf /var/lib/apt/lists/*

# Python 패키지
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# 소스 코드 복사
WORKDIR /app
COPY *.py ./
COPY tests/ ./tests/