# Use python image
FROM python:3.11-alpine

# Use `docker-cron` as the base image
# Copy the script into the container
COPY main.py /app/

# Install required packages
RUN apk add --no-cache openssl openssl-dev
RUN pip install pyOpenSSL

# Set the working directory
WORKDIR /app
