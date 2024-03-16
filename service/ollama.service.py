import ollama
import requests

def getCompletionResponse(prompt, model='mistral'):
    url = 'http://localhost:PORT/api/generate'
    payload = {
        model: model,
        prompt: prompt
    }
    response = requests.post(url, json=payload)
    return response
