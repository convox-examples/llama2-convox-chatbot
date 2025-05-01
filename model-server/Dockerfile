# model_server/Dockerfile
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04 as base

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install vLLM and other requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .
COPY download_model.py .

# Create model directory
RUN mkdir -p /app/models

# Download model during build (ARG will be passed from convox build)
ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}
# Download the model if HF_TOKEN is provided, otherwise it will be mounted
RUN if [ ! -z "$HF_TOKEN" ]; then \
      python3 download_model.py; \
    else \
      echo "HF_TOKEN not provided, skipping model download. Model will be mounted at runtime."; \
    fi

# Set environment variables
ENV MODEL_PATH=/app/models
ENV MAX_TOKENS=512

# Run the server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]