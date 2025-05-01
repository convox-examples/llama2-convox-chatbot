# Llama 2 Chatbot with Convox

This repository contains a complete, production-ready AI chatbot application built with Meta's Llama 2 7B language model, designed for seamless deployment on Convox infrastructure.

## 📋 Overview

This application provides a scalable, containerized AI assistant powered by the Llama 2 7B chat model. It features:

- A lightweight React frontend for user interaction
- A FastAPI service for handling chat session management
- A GPU-accelerated inference server running the Llama 2 model
- Fully containerized deployment supporting NVIDIA GPUs
- Ready for production deployment via Convox

## 🏗️ Architecture

The application is structured into three main services:

### 1. Frontend (React)
- Simple, intuitive chat interface
- Persistent chat sessions
- Responsive design with real-time feedback

### 2. API Service (FastAPI)
- Handles chat session management
- Manages message history
- Communicates with the model server
- Provides a RESTful API interface

### 3. Model Server (vLLM + Llama 2)
- Runs the Llama 2 7B chat model
- GPU-accelerated inference using vLLM
- Optimized for low-latency responses
- Configurable generation parameters

## 🚀 Deployment with Convox

This project is pre-configured for easy deployment on Convox. The `convox.yml` file contains all necessary configuration to deploy the application with appropriate resource allocations.

### Prerequisites

1. A Convox account and Rack
2. GPU-enabled nodes in your Convox Rack (for the model server)
3. Hugging Face access token with permission to download Llama 2 models

### Deployment Steps

1. **Configure Node Groups**

   Ensure your Convox Rack has a node group with GPU support. You can add a GPU-enabled node group with:

   ```bash
   convox rack params set additional_node_groups_config='[{"type":"g4dn.xlarge","min_size":1,"max_size":1,"label":"alternate-test-tag-2"}]' -r <your-rack>
   ```

2. **Set Environment Variables**

   Set your Hugging Face token:

   ```bash
   convox env set HF_TOKEN=<your-hugging-face-token> -a <your-app>
   ```

3. **Deploy the Application**

   ```bash
   convox deploy
   ```

4. **Access Your Application**

   After deployment, you can access your chatbot at the URL provided by Convox:

   ```bash
   convox services
   ```

## 📊 Resource Allocation

The application is configured with the following resource allocations:

- **Model Server**: 
  - 1 vCPU
  - 8GB RAM
  - 1 GPU
  - Persistent volume for model storage

- **API Service**:
  - 0.25 vCPU
  - 512MB RAM
  - 2 replicas for high availability

- **Frontend**:
  - 0.25 vCPU
  - 256MB RAM
  - 2 replicas for high availability

These values can be adjusted in the `convox.yml` file based on your specific needs and traffic expectations.

## 🧰 Development

### Prerequisites

- Docker and Docker Compose
- Node.js 16+ for frontend development
- Python 3.9+ for backend development
- NVIDIA GPU with CUDA support (for local model server testing)

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/llama2-convox-chatbot.git
   ```

2. Start the services using Docker Compose:
   ```bash
   docker-compose up
   ```

3. Access the application at http://localhost:3000

## 📄 License

This project is released under the MIT License.

## ⚠️ Important Notes

- You need access to Meta's Llama 2 model on Hugging Face. Request access at https://huggingface.co/meta-llama/Llama-2-7b-chat-hf
- GPU resources are required for the model server
- The model server will download approximately 14GB of model weights

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📚 References

- [Convox Documentation](https://docs.convox.com/)
- [Llama 2 Documentation](https://ai.meta.com/llama/)
- [vLLM Project](https://github.com/vllm-project/vllm)