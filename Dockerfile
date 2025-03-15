FROM python:3.10-slim-buster

# Install system dependencies (for psycopg2, etc.)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

EXPOSE 8000

# Use the entrypoint script to seed data and start the app
CMD ["/app/entrypoint.sh"]
