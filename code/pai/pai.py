# SPDX-FileCopyrightText: 2025 Hewlett Packard Enterprise Development LP
# SPDX-License-Identifier: MIT

# Private AI Chatbot

import argparse
import json
import sys
from typing import List

import requests

API_URL = "http://127.0.0.1:11434/api"
DEFAULT_MODEL = "deepseek-r1:32b"


def fetch_models() -> List[str]:
    try:
        response = requests.get(f"{API_URL}/tags", timeout=5)
        response.raise_for_status()
        data = response.json()
        return [item["name"] for item in data.get("models", [])]
    except Exception as exc:
        print(f"Warning: failed to fetch models ({exc}).")
        return []


def show_models(models: List[str]) -> None:
    if not models:
        print("No models discovered.")
    else:
        print("Available models:")
        for name in models:
            print(f"  - {name}")


def stream_prompt(model: str, prompt: str) -> None:
    payload = {"model": model, "prompt": prompt}
    with requests.post(f"{API_URL}/generate", json=payload, stream=True) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            data = json.loads(line)
            if chunk := data.get("response"):
                print(chunk, end="", flush=True)
            if data.get("done"):
                print()
                break


def chat_loop(model: str) -> None:
    print("Private AI chat. Type /exit to quit.")
    models = fetch_models()
    show_models(models)
    history = ""
    while True:
        user = input("You: ").strip()
        if user.lower() in {"/exit", "/quit"}:
            break
        history += f"User: {user}\nAssistant:"
        print("Private AI:", end=" ")
        stream_prompt(model, history)
        history += "\nAssistant: "


def main() -> None:
    parser = argparse.ArgumentParser(description="Private AI CLI")
    parser.add_argument("prompt", nargs="*", help="One-shot prompt text.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name to use.")
    parser.add_argument("--chat", action="store_true", help="Start interactive chat session.")
    args = parser.parse_args()

    models = fetch_models()
    show_models(models)
    model = args.model

    if args.chat:
        chat_loop(model)
    else:
        text = " ".join(args.prompt) if args.prompt else "Hello from Private AI"
        stream_prompt(model, text)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
