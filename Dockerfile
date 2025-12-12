# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Set timezone to UTC (CRITICAL for TOTP)
ENV TZ=UTC
WORKDIR /app

# Install cron and timezone tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata && \
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo UTC > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy packages, code, and keys
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY app/ app/
COPY scripts/ scripts/
COPY cron/ cron/
COPY student_private.pem .
COPY instructor_public.pem .

# 1. Ensure scripts are executable and app files are readable (Permission fix)
RUN chmod -R +rx scripts/ && \
    chmod -R +r app/

# Setup cron job: Set permissions on the file and install it into crontab
# DELETE the failing RUN command entirely:
# RUN chmod 0644 cron/2fa-cron && cat cron/2fa-cron | crontab -

# Create persistent volume directories
RUN mkdir -p /data /cron && chmod 755 /data /cron
# ...

EXPOSE 8080

# Start cron daemon and the API server
CMD ["sh", "-c", "cron && uvicorn app.api_server:app --host 0.0.0.0 --port 8080"]