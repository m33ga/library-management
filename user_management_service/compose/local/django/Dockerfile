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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy all requirements files
COPY requirements/ /app/requirements/
RUN pip install --upgrade pip && pip install -r /app/requirements/local.txt

# Copy the Django project files into the container
COPY . /app

# Set up the entrypoint
ENTRYPOINT ["python", "user_management/manage.py"]

# Default command
CMD ["runserver", "0.0.0.0:8000"]
