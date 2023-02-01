# Use python image
FROM python:3.12.0a4-buster

# Use `docker-cron` as the base image
# Copy the script into the container
COPY main.py /app/
COPY domains.txt /app/
COPY sample.env /app/

# Install required packages
RUN apt-get update && apt-get install openssl openssl-dev
RUN pip install pyOpenSSL python-dotenv

# Set the working directory
WORKDIR /app
