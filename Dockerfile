FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python files
COPY . .

# Default command (will be overridden in docker-compose)
CMD ["python", "server_data.py.py"]