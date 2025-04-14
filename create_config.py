#!/usr/bin/env python3
"""
Script to create a config.toml file for OpenManus using the ChatGLM model via Ollama.
"""
import os
import shutil
from pathlib import Path

def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).resolve().parent

def main():
    project_root = get_project_root()
    config_dir = project_root / "config"
    example_path = config_dir / "config.example.toml"
    config_path = config_dir / "config.toml"
    
    if not example_path.exists():
        print(f"Error: Example config file not found at {example_path}")
        return
    
    # Create config content for Ollama with ChatGLM
    config_content = """# Global LLM configuration for ChatGLM via Ollama
[llm]
api_type = "ollama"
model = "EntropyYue/chatglm3:latest"
base_url = "http://localhost:11434/v1"
api_key = "ollama"
max_tokens = 4096
temperature = 0.0

# Optional configuration for search settings
[search]
engine = "Google"
"""
    
    # Write the new config file
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    print(f"Created config file at {config_path}")
    print("Configuration set to use EntropyYue/chatglm3:latest model via Ollama")

if __name__ == "__main__":
    main()
