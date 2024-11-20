# Stage 1: Builder Stage
FROM docker.io/python:3.12.7-slim-bookworm AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pip and dependencies
COPY requirements/ /app/requirements/
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements/production.txt

# Copy application code for dependency analysis
COPY . /app

# Stage 2: Final Production Stage
FROM docker.io/python:3.12.7-slim-bookworm AS runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy Django application code
COPY . /app

# Expose the application port
EXPOSE 8080

# Set the entrypoint

ENTRYPOINT ["/bin/sh", "-c", "cd notification && gunicorn notification.wsgi:application --bind 0.0.0.0:8080"]