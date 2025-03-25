FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy all workdir files
COPY . /app

# Define build arguments with default values
ARG WORKERS=8
ARG TIMEOUT_KEEP_ALIVE=300

# Set environment variables from build arguments
ENV WORKERS=$WORKERS \
    TIMEOUT_KEEP_ALIVE=$TIMEOUT_KEEP_ALIVE

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc \
    && rm -rf /var/lib/apt/lists/*

# Expose port
EXPOSE 8000

# Some logs
RUN echo "WORKERS: $WORKERS"
RUN echo "TIMEOUT_KEEP_ALIVE: $TIMEOUT_KEEP_ALIVE"

# Command to run the application using environment variables
CMD uvicorn main:app --host 0.0.0.0 --port 8000 --workers $WORKERS --timeout-keep-alive $TIMEOUT_KEEP_ALIVE