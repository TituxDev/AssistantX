"""
agent.py
LLM agent with support for multiple providers.

The Agent class provides a common interface for interacting with
different LLM providers while handling provider-specific request
and response formats internally.
"""

import requests
import os

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / "config" / ".env")

class Agent:
    class Provider:
        def __init__(self, url, models):
            self.url= url
            self.models= models
    available_models={
        "ollama": Provider("http://localhost:11434/api/chat", ["llama3.1:latest", "llama3.2:1b"]),
        "gemini": Provider("https://generativelanguage.googleapis.com/v1beta/models/", ["gemini-3.1-flash-lite"])
    }

    def __init__(self, model):
        self.update_model(model)
        self.system= ""
        self.history= []
    
    def update_model(self, model):
        for provider, info in self.available_models.items():
            if model in info.models:
                self.model= model
                self.provider= provider
                self.url= info.url
                self.api= getattr(self, provider)
                break
        else:
            raise ValueError(f"Model {model} is not available")

    def call(self, message):
        connection= self.api(message, "build request")
        try:
            response= requests.post(connection[0], json=connection[1])
        except requests.exceptions.RequestException:
            raise RuntimeError("Could not communicate with the provider.")
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise RuntimeError("Provider rejected request")
        return response

    def chat(self, message):
        response= self.call(message)
        try:
            response= self.api(response, "filter response")
        except (AttributeError, TypeError, KeyError, IndexError) as e:
            raise RuntimeError("Invalid response received from provider.") from e
        self.history.append(self.api(message, "message register"))
        self.history.append(self.api(response, "response register"))
        return response

    def ollama(self, message, mode):
        match mode:
            case "build request":
                return ( self.url ,
                        {
                            "model": self.model,
                            "messages": [
                                {"role": "system", "content": self.system},
                                *self.history,
                                {"role": "user", "content": message}
                            ],
                            "stream": False
                        }
                    )
            case "filter response":
                return message.json()["message"]["content"]
            case "message register":
                return {"role": "user", "content": message}
            case "response register":
                return {"role": "assistant", "content": message}

    def gemini(self, message, mode):
        match mode:
            case "build request":
                return (self.url + f"{self.model}:generateContent?key={os.environ['DEFAULT_GEMINI_API_KEY']}" ,
                    {
                        "system_instruction": {
                            "parts": [{"text": self.system}]
                        },
                        "contents": [
                            *self.history,
                            {"role": "user", "parts": [{"text": message}]}
                        ]
                    }
                )
            case "filter response":
                return message.json()["candidates"][0]["content"]["parts"][0]["text"]
            case "message register":
                return {"role": "user", "parts": [{"text": message}]}
            case "response register":
                return {"role": "model", "parts": [{"text": message}]}

if __name__ == "__main__":
    print("Available models:")
    for provider, info in Agent.available_models.items():
        print(f"----\n[{provider}]\n{info.models}")

    while True:
        try:
            agent= Agent(input(f"Select a model: "))
            break
        except ValueError as e:
            print(e)

    while (message:= input("user: ")) != "\\exit":
        print(f"agent: {agent.chat(message)}")