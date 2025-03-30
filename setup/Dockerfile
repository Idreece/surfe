FROM python:3.11-slim

WORKDIR /app

# Install only psycopg2 dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Set working directory
WORKDIR /app

# Set Python path
ENV PYTHONPATH=/app

# Command to keep container running
CMD ["bash"] 