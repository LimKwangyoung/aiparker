# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Disable Python output buffering
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    vim \
    gcc \
    g++ \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    awscli \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the source code
COPY src /app/src

# Copy the certs (provided by Jenkins)
COPY cert /app/cert

# Configure AWS CLI
RUN mkdir -p ~/.aws && \
    echo "[default]\nregion = ap-northeast-2\noutput = json" > ~/.aws/config && \
    echo "[default]\naws_access_key_id = $(cat /app/cert/aws_access_key_id.txt)\naws_secret_access_key = $(cat /app/cert/aws_secret_access_key.txt)" > ~/.aws/credentials

# Create images directory
RUN mkdir -p /app/images

# Expose port for MQTT
EXPOSE 8883

# Command to run the application
CMD ["python3", "/app/src/execute_ocr_docker.py"]