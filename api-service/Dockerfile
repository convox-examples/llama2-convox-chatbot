# api_service/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Run the API server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]