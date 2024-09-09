# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Disable Python output buffering
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    awscli

# Install Python dependencies globally
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy sources
COPY . .

# 스크립트에 실행 권한을 부여합니다.
RUN chmod +x /app/download_s3.sh

# Configure AWS CLI
RUN mkdir -p ~/.aws && \
    echo "[default]\nregion = ap-northeast-2\noutput = json" > ~/.aws/config && \
    echo "[default]\naws_access_key_id = $(cat /app/cert/aws_access_key_id.txt)\naws_secret_access_key = $(cat /app/cert/aws_secret_access_key.txt)" > ~/.aws/credentials

# Create images directory
RUN mkdir -p /app/images

# Expose port for MQTT
EXPOSE 8883

# Command to run the application
CMD ["python", "/app/check_parking.py"]