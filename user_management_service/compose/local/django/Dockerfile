# Use Python 3.12.7 slim-bookworm as the base image
FROM docker.io/python:3.12.7-slim-bookworm AS python

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    wait-for-it \
    # Translations dependencies
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy all requirements files
COPY requirements/ /app/requirements/
RUN pip install --upgrade pip && pip install -r /app/requirements/local.txt


COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Copy the Django project files into the container
COPY . /app

# Set up the entrypoint
ENTRYPOINT ["/entrypoint"]
