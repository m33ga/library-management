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
COPY notification_service/requirements/ /app/requirements/
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

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    wait-for-it \
    # Translations dependencies
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --chown=django:django notification_service/compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


COPY --chown=django:django notification_service/compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy application code to WORKDIR
COPY --chown=django:django . /app

# make django owner of the WORKDIR directory as well.
RUN chown -R django:django /app

USER django

ENTRYPOINT ["/entrypoint"]
