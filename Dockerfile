# ----------------------------------------------------------------------
# Stage 1: Builder - Installs Python dependencies
# ----------------------------------------------------------------------
FROM python:3.11-slim AS builder
WORKDIR /app
# Copy the file listing all dependencies
COPY requirements.txt .
# Install dependencies into the builder's environment
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------------------------
# Stage 2: Runtime - Creates the minimal final image
# ----------------------------------------------------------------------
FROM python:3.11-slim

# Set timezone to UTC (CRITICAL for TOTP time synchronization)
ENV TZ=UTC
WORKDIR /app

# Install system dependencies: cron and timezone tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata && \
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo UTC > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code and keys to the /app directory
COPY app/ app/
COPY scripts/ scripts/
COPY cron/ cron/
COPY student_private.pem .
COPY instructor_public.pem .

# ----------------------------------------------------------------------
# Final Configuration and Startup
# ----------------------------------------------------------------------

# 1. Ensure scripts are executable and app files are readable (Permission fix)
RUN chmod -R +rx scripts/ && \
    chmod -R +r app/

# 2. Setup cron job: Set permissions on the file and install it into crontab
# Using 'cat | crontab -' prevents issues with Windows CRLF line endings
RUN chmod 0644 cron/2fa-cron && cat cron/2fa-cron | crontab -

# 3. Create persistent volume mount points and set permissions
RUN mkdir -p /data /cron && chmod 755 /data /cron

EXPOSE 8080

# 4. Start both cron daemon and the API server
CMD ["sh", "-c", "cron && uvicorn app.api_server:app --host 0.0.0.0 --port 8080"]