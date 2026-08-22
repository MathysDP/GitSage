import requests
import sys
import subprocess
import json
import pyperclip

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

def generate_commit_message(diff, config):
    response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen3:8b",
        "system": config["prompt"],
        "prompt": f"Analyze this staged git diff:\n\n{diff}",
        "stream": True,
        "think": False,
    },
    stream=True,
    )
    output = ""
    for line in response.iter_lines():
        if not line:
            continue
        data = json.loads(line)
        if data.get("response") != "":
            output += data["response"]
            print(data["response"], end="", flush=True)
    print()
    return output

def draw_logo():
    GREEN = "\033[38;5;71m"
    RESET = "\033[0m"

    print(f"""{GREEN}
                              ████████
                              ██    ██
        ████                  ██    ██
           ███                ████████
             ███                 █
               ███               █     ████████
                 ████            ████████    ██
               ███               █     ██    ██
             ███                 █     ████████
           ███                ███████
         ███                  ██   ██
                              ██   ██
            ████████████      ███████{RESET}
""")

def copy_to_clipboard(text):
    try:
        pyperclip.copy(text)
        print("[INFO] Output copied to clipboard.")
    except pyperclip.PyperclipException:
        print(f"[ERROR] Failed to copy to clipboard.\n [WARNING] Ensure you have a clipboard utility installed !")

def print_help():
    print("Usage: gitsage <command> <options>\n")
    print("Commands:\n")
    print("  help              Show this help message")
    print("  commit            Generate a commit message based on the staged changes\n")
    print("Options:\n")
    print("  --copy            Copy the output to the clipboard")