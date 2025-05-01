# download_model.py
import os
import sys
import subprocess

def download_model():
    # Ensure Hugging Face credentials are set
    if not os.environ.get("HF_TOKEN"):
        print("Error: HF_TOKEN environment variable not set.")
        print("Please set it to your Hugging Face token with access to Llama 2.")
        sys.exit(1)
        
    model_name = "meta-llama/Llama-2-7b-chat-hf"
    output_dir = "/app/models/llama-2-7b-chat"
    
    print(f"Downloading {model_name} to {output_dir}...")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Download the model using Hugging Face CLI
    subprocess.run([
        "python", "-m", "huggingface_hub", "download",
        "--repo-id", model_name,
        "--local-dir", output_dir,
        "--token", os.environ["HF_TOKEN"]
    ])
    
    print(f"Model downloaded successfully to {output_dir}")

if __name__ == "__main__":
    download_model()