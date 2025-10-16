# SPDX-FileCopyrightText: 2025 Hewlett Packard Enterprise Development LP
# SPDX-License-Identifier: MIT

# Private AI Chatbot

import argparse
import json
import re
import sys
import urllib.parse
from typing import List, Tuple, Optional

import requests

API_URL = "http://127.0.0.1:11434/api"
DEFAULT_MODEL = "deepseek-r1:32b"


def extract_github_urls(text: str) -> List[str]:
    """Extract GitHub URLs from text using regex patterns."""
    # Pattern to match GitHub URLs (repositories, files, directories)
    # This pattern is more precise and handles trailing punctuation
    github_pattern = r'https://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+(?:/[a-zA-Z0-9_./%-]*)?'
    urls = re.findall(github_pattern, text)
    
    # Clean up URLs by removing trailing punctuation that might not be part of the URL
    cleaned_urls = []
    for url in urls:
        # Remove trailing punctuation that's likely not part of the URL
        url = re.sub(r'[.,;:!?]$', '', url.strip())
        cleaned_urls.append(url)
    
    return list(set(cleaned_urls))  # Remove duplicates


def convert_github_url_to_raw(url: str) -> Tuple[str, str]:
    """Convert GitHub URLs to raw content URLs and determine content type."""
    # Parse the URL to extract components
    parsed = urllib.parse.urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    
    if len(path_parts) < 2:
        return url, "unknown"
    
    owner, repo = path_parts[0], path_parts[1]
    
    # Handle different GitHub URL types
    if len(path_parts) == 2:
        # Repository root - get README or main files
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        return api_url, "directory"
    elif len(path_parts) >= 4 and path_parts[2] in ['blob', 'tree']:
        branch_or_commit = path_parts[3]
        file_path = '/'.join(path_parts[4:]) if len(path_parts) > 4 else ''
        
        if path_parts[2] == 'blob':
            # Single file
            if file_path:
                raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch_or_commit}/{file_path}"
                return raw_url, "file"
            else:
                # Branch root
                api_url = f"https://api.github.com/repos/{owner}/{repo}/contents?ref={branch_or_commit}"
                return api_url, "directory"
        elif path_parts[2] == 'tree':
            # Directory
            if file_path:
                api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch_or_commit}"
            else:
                api_url = f"https://api.github.com/repos/{owner}/{repo}/contents?ref={branch_or_commit}"
            return api_url, "directory"
    
    return url, "unknown"


def fetch_github_content(url: str) -> Optional[str]:
    """Fetch content from GitHub URLs."""
    try:
        raw_url, content_type = convert_github_url_to_raw(url)
        
        if content_type == "file":
            # Fetch raw file content
            response = requests.get(raw_url, timeout=10)
            response.raise_for_status()
            return f"\n--- Content from {url} ---\n{response.text}\n--- End of {url} ---\n"
        
        elif content_type == "directory":
            # Fetch directory listing via GitHub API
            response = requests.get(raw_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            content = f"\n--- Directory listing from {url} ---\n"
            if isinstance(data, list):
                # Directory contents
                for item in data[:20]:  # Limit to first 20 items
                    item_type = item.get('type', 'unknown')
                    item_name = item.get('name', 'unknown')
                    content += f"  {item_type}: {item_name}\n"
                    
                    # For Python files and important files, fetch content
                    if (item_type == 'file' and 
                        (item_name.endswith('.py') or 
                         item_name.endswith('.md') or 
                         item_name.endswith('.json') or 
                         item_name in ['README', 'LICENSE', 'setup.py', 'requirements.txt'])):
                        
                        if item.get('download_url'):
                            try:
                                file_response = requests.get(item['download_url'], timeout=5)
                                file_response.raise_for_status()
                                content += f"\n    Content of {item_name}:\n"
                                # Limit file content to prevent overwhelming output
                                file_content = file_response.text
                                if len(file_content) > 2000:
                                    content += file_content[:2000] + "\n    [Content truncated...]\n"
                                else:
                                    content += file_content + "\n"
                            except Exception as e:
                                content += f"    [Error fetching {item_name}: {e}]\n"
            else:
                # Single file info
                content += f"File: {data.get('name', 'unknown')}\n"
                if data.get('download_url'):
                    try:
                        file_response = requests.get(data['download_url'], timeout=5)
                        file_response.raise_for_status()
                        content += f"\nContent:\n{file_response.text}\n"
                    except Exception as e:
                        content += f"[Error fetching content: {e}]\n"
            
            content += f"--- End of {url} ---\n"
            return content
        
        else:
            return f"\n--- Unable to fetch content from {url} (unsupported URL format) ---\n"
            
    except Exception as e:
        return f"\n--- Error fetching content from {url}: {e} ---\n"


def enhance_prompt_with_github_content(prompt: str) -> str:
    """Detect GitHub URLs in prompt and enhance with their content."""
    github_urls = extract_github_urls(prompt)
    
    if not github_urls:
        return prompt
    
    enhanced_prompt = prompt
    github_content = ""
    
    print(f"Detected {len(github_urls)} GitHub URL(s), fetching content...")
    
    for url in github_urls:
        print(f"  Fetching: {url}")
        content = fetch_github_content(url)
        if content:
            github_content += content
    
    if github_content:
        enhanced_prompt += "\n\n" + github_content
        print("GitHub content added to prompt.")
    
    return enhanced_prompt


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


def stream_prompt(model: str, prompt: str) -> str:
    """Stream AI response and return the complete response text."""
    payload = {"model": model, "prompt": prompt}
    complete_response = ""
    
    with requests.post(f"{API_URL}/generate", json=payload, stream=True) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            data = json.loads(line)
            if chunk := data.get("response"):
                print(chunk, end="", flush=True)
                complete_response += chunk
            if data.get("done"):
                print()
                break
    
    return complete_response


def chat_loop(model: str) -> None:
    print("Private AI chat. Type /exit to quit.")
    models = fetch_models()
    show_models(models)
    history = ""
    while True:
        user = input("You: ").strip()
        if user.lower() in {"/exit", "/quit"}:
            break
        
        # Enhance user input with GitHub content if URLs are present
        enhanced_user_input = enhance_prompt_with_github_content(user)
        
        history += f"User: {enhanced_user_input}\nAssistant: "
        print("Private AI:", end=" ")
        ai_response = stream_prompt(model, history)
        history += ai_response + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Private AI CLI for Ollama.")
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
        text = " ".join(args.prompt) if args.prompt else "Hello from Private AI."
        # Enhance one-shot prompt with GitHub content if URLs are present
        enhanced_text = enhance_prompt_with_github_content(text)
        stream_prompt(model, enhanced_text)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)


def test_github_parsing():
    """Test function to validate GitHub URL parsing with the provided examples."""
    test_urls = [
        "https://github.com/opencomputeproject/ocp-diag-core/tree/main/json_spec",
        "https://github.com/opencomputeproject/ocp-diag-core/tree/main/json_spec/output", 
        "https://github.com/opencomputeproject/ocp-diag-core-python",
        "https://github.com/opencomputeproject/ocp-diag-quickstart/tree/main/python",
        "https://github.com/opencomputeproject/ocp-diag-pci_lmt/blob/dev/src/pci_lmt/results.py"
    ]
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        raw_url, content_type = convert_github_url_to_raw(url)
        print(f"  Raw URL: {raw_url}")
        print(f"  Content type: {content_type}")
        
    # Test URL extraction from text
    test_text = """
    Check out the spec text https://github.com/opencomputeproject/ocp-diag-core/tree/main/json_spec
    the json schema https://github.com/opencomputeproject/ocp-diag-core/tree/main/json_spec/output
    the api https://github.com/opencomputeproject/ocp-diag-core-python
    the python quickstarts https://github.com/opencomputeproject/ocp-diag-quickstart/tree/main/python
    this diag as an example https://github.com/opencomputeproject/ocp-diag-pci_lmt/blob/dev/src/pci_lmt/results.py
    """
    
    print(f"\nExtracting URLs from text:")
    extracted_urls = extract_github_urls(test_text)
    for url in extracted_urls:
        print(f"  Found: {url}")
    
    print(f"\nTotal URLs found: {len(extracted_urls)}")


# Uncomment the next line to run tests manually
# test_github_parsing()
