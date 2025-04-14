#!/usr/bin/env python3
"""
Script to update config.toml file for OpenManus to use Qwen2.5 model via Ollama.
"""
import os
from pathlib import Path

def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).resolve().parent

def main():
    project_root = get_project_root()
    config_dir = project_root / "config"
    config_path = config_dir / "config.toml"
    
    # Create config content for Ollama with Qwen2.5
    config_content = """# Global LLM configuration for Qwen2.5 via Ollama (with tool calling support)
[llm]
api_type = "ollama"
model = "qwen2.5:3b"
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
    
    print(f"Updated config file at {config_path}")
    print("Configuration set to use qwen2.5:3b model via Ollama")
    print("This model supports tool calling functionality")

if __name__ == "__main__":
    main()
