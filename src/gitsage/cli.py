import gitsage.utils as utils
import sys

def main():
    if not utils.check_ollama():
        print("[ERROR] Ollama is not running.\nTry:\n\t> ollama pull 'your model'")
        sys.exit(1)
    # utils.draw_logo()
    config = utils.load_config()
    diff = utils.get_diff()
    utils.generate_commit_message(diff, config)
