import requests
import sys
import subprocess
import json
import pyperclip
from pathlib import Path
import toml
import os
from importlib.metadata import version

def load_config():
    DEFAULT_CONFIG = '''\
model = "qwen3:8b"
prompt = """You generate Git commit messages.\n\nAnalyze the following staged git diff.\n\nReturn ONLY a single Conventional Commit message.\nFormat:\ntype(scope): description\n\nRules:\n- Use feat, fix, refactor, docs, test, chore, or perf\n- Keep the description concise\n- Use imperative mood\n- Do not invent changes\n- Do not include markdown\n\n"""
ollama_url = "http://localhost:11434"
'''

    config_path = Path.home() / ".config/gitsage/config.toml"
    if not os.path.exists(config_path):
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            f.write(DEFAULT_CONFIG)
    try:
        with open(config_path, "r") as f:
            return toml.load(f)
    except FileNotFoundError:
        print_error(f"Config file not found at {config_path}.")
        sys.exit(1)
    except toml.TomlDecodeError:
        print_error("Invalid TOML in config.toml.")
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
        print_error(f"Failed to get git diff: {e}")
        sys.exit(1)

def generate_commit_message(diff, config):
    response = requests.post(
        config["ollama_url"] + "/api/generate",
        json={
            "model": config["model"],
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
        print()
        print_info("Output copied to clipboard.")
    except pyperclip.PyperclipException:
        print_error(f"Failed to copy to clipboard.\n")
        print_warning("Ensure you have a clipboard utility installed !")

def print_help():
    print("Usage: gitsage <command> <options>\n")
    print("Commands:\n")
    print("  help                   Show this help message")
    print("  commit                 Generate a commit message based on the staged changes")
    print("  version/-v/--version   Show the version of GitSage\n")
    print("Options:\n")
    print("  --copy            Copy the output to the clipboard")


def print_version():
    print(f"GitSage v{version('gitsage')}")

def print_error(message):
    RED = "\033[31m"
    RESET = "\033[0m"
    print(f"{RED}[ERROR]: {message}{RESET}")

def print_warning(message):
    YELLOW = "\033[33m"
    RESET = "\033[0m"
    print(f"{YELLOW}[WARNING]: {message}{RESET}")

def print_info(message):
    BLUE = "\033[34m"
    RESET = "\033[0m"
    print(f"{BLUE}[INFO]: {message}{RESET}")
