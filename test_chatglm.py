#!/usr/bin/env python3
"""
Simple test script to verify that the ChatGLM model is working via Ollama's OpenAI-compatible API.
"""
import sys
import json
import requests

def test_ollama_chatglm():
    """Test the ChatGLM model via Ollama's OpenAI-compatible API."""
    
    # Ollama API endpoint for chat completions
    url = "http://localhost:11434/v1/chat/completions"
    
    # Request headers
    headers = {
        "Content-Type": "application/json"
    }
    
    # Request payload
    payload = {
        "model": "EntropyYue/chatglm3:latest",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "请用中文回答：你是什么模型？你有什么功能？"}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    print("Sending request to Ollama API...")
    
    try:
        # Send the request
        response = requests.post(url, headers=headers, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response
            result = response.json()
            
            # Extract and print the assistant's message
            assistant_message = result["choices"][0]["message"]["content"]
            print("\nResponse from ChatGLM:\n")
            print(assistant_message)
            print("\n" + "-"*50)
            print("Test completed successfully!")
            return True
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing ChatGLM via Ollama...")
    success = test_ollama_chatglm()
    sys.exit(0 if success else 1)
