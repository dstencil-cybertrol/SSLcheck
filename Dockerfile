# Use python image
FROM python:3.11-alpine

# Use `docker-cron` as the base image
FROM abiosoft/cron:latest

# Copy the script into the container
COPY main.py /app/

# Install required packages
RUN apk add --no-cache openssl openssl-dev
RUN pip install pyOpenSSL

# Set the working directory
WORKDIR /app

# Set the CRON schedule environment variable
ENV CRON_SCHEDULE "0 0 * * 1"

# Run the script using `cron`
CMD ["cron", "-f"]
