import gitsage.utils as utils
import sys

def commit(copy=False):
    if not utils.check_ollama():
        utils.print_error("Ollama is not running.\nTry:\n\t> ollama pull 'your model'")
        sys.exit(1)
    config = utils.load_config()
    diff = utils.get_diff()
    commit = utils.generate_commit_message(diff, config)
    if copy:
        utils.copy_to_clipboard(commit)

def main():
    if len(sys.argv) < 2:
        utils.draw_logo()
        utils.print_help()
        return 1

    if sys.argv[1] in ["help", "-h", "--help"]:
        utils.draw_logo()
        utils.print_help()
        return 0

    if sys.argv[1] in ["version", "-v", "--version"]:
        utils.print_version()
        return 0

    command = sys.argv[1]
    copy = sys.argv[2] == "--copy" if len(sys.argv) > 2 else False

    if command == "commit":
        commit(copy=copy)
    else:
        utils.print_error(f"Unknown command: {command}\n")
        print("Usage: gitsage <command> <options>")
        return 1
