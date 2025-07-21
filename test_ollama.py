# Ollama Test Script
import requests
import json

def test_ollama():
    try:
        # Test API connection
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        print(f"API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            print(f"Available models: {len(models)}")
            
            for model in models:
                print(f"- {model['name']} ({model['size']/1000000000:.1f}GB)")
        
        # Test generation
        test_prompt = "Hello, this is a test"
        gen_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": test_prompt,
                "stream": False
            },
            timeout=30
        )
        
        if gen_response.status_code == 200:
            result = gen_response.json()
            print(f"\nGeneration test successful!")
            print(f"Response: {result['response'][:100]}...")
        else:
            print(f"Generation failed: {gen_response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ollama()
