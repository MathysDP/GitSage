import requests
import sys
import subprocess
import json


def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[ERROR] config.json not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON in config.json.")
        sys.exit(1)

# config = load_config()

def check_ollama():
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=2
        )
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

# if not check_ollama():
#     print("[ERROR] Ollama is not running.\nTry:\n\t> ollama pull 'your model'")
#     sys.exit(1)

def get_diff():
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to get git diff: {e}")
        sys.exit(1)

# diff = get_diff()

def generate_commit_message(diff, config):
    response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen3:8b",
        "system": config["prompt"],
        "prompt": f"Analyze this staged git diff:\n\n{diff}",
        "stream": True,
    },
    stream=True,
    )
