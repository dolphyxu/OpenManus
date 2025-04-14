#!/usr/bin/env python3
"""
Test script to verify that OpenManus can interact with the ChatGLM model via Ollama.
This script uses OpenManus's LLM module directly, bypassing the full flow system.
"""
import asyncio
import sys
from typing import Dict, Optional

# Import OpenManus modules
try:
    from app.config import LLMSettings
    from app.llm import LLM
    from app.schema import Message
    print("Successfully imported OpenManus modules")
except ImportError as e:
    print(f"Error importing OpenManus modules: {e}")
    print("Make sure all dependencies are installed")
    sys.exit(1)

async def test_openmanus_llm():
    """Test OpenManus's LLM module with ChatGLM via Ollama."""
    
    # Create LLM settings for ChatGLM via Ollama
    llm_settings = LLMSettings(
        model="EntropyYue/chatglm3:latest",
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        api_type="ollama",
        api_version="",
        max_tokens=4096,
        temperature=0.7
    )
    
    # Create LLM instance with custom settings
    llm_config: Dict[str, LLMSettings] = {"chatglm": llm_settings}
    llm = LLM("chatglm", llm_config.get("chatglm"))
    
    # Create messages
    system_msg = Message.system_message("You are a helpful AI assistant.")
    user_msg = Message.user_message("请用中文回答：你是什么模型？你能做什么？")
    
    try:
        print("Sending request to ChatGLM via OpenManus LLM module...")
        
        # Call the LLM
        response = await llm.ask(
            messages=[user_msg],
            system_msgs=[system_msg],
            stream=False
        )
        
        print("\nResponse from ChatGLM:\n")
        print(response)
        print("\n" + "-"*50)
        print("Test completed successfully!")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing OpenManus LLM module with ChatGLM...")
    success = asyncio.run(test_openmanus_llm())
    sys.exit(0 if success else 1)
