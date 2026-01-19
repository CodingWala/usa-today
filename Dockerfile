FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Set IST timezone
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app ./app

# Create data & log dirs
RUN mkdir -p /data /var/log \
    && chmod 755 /data /var/log

# Create non-root user for python execution
RUN useradd -m appuser

# Cron job
COPY cron/scraper-cron /etc/cron.d/scraper-cron
RUN chmod 0644 /etc/cron.d/scraper-cron \
    && crontab /etc/cron.d/scraper-cron

# Ensure cron log exists
RUN touch /var/log/cron.log

# IMPORTANT: Run cron as ROOT
CMD ["cron", "-f"]
