import gitsage.utils as utils
import sys

def commit():
    if not utils.check_ollama():
        print("[ERROR] Ollama is not running.\nTry:\n\t> ollama pull 'your model'")
        sys.exit(1)
    config = utils.load_config()
    diff = utils.get_diff()
    utils.generate_commit_message(diff, config)

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["help", "-h", "--help"]:
        utils.draw_logo()
        utils.print_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "commit":
        commit()
    else:
        print(f"Unknown command: {command}\n")
        print("Use 'gitsage help' to see available commands.")
        sys.exit(1)
