# GitSage
![logo](ressources/logo.png)

Local AI powered commit generator based on ur repository local change.

## Installation

### Prerequirements

    - Python>=3.10
    - Python3-pip or pipx
    - Python3-venv (optional if using pipx)
    - Ollama
    - utilitaire de commande pour gérer le presse-papier (ex: wl_clipboard, xclip, pbcopy, clip, etc..)

#### Start Ollama

```bash
$> ollama pull qwen3:8b (or the model of your choice)
```

#### Create your virtual environnent (if using pip)

```bash
$> python3 -m venv .venv
```

##### Use your virtual environnement

```bash
$> source .venv/bin/activate
```

### Install GitSage

#### with pip :

```bash
(.venv) $> pip install gitsage-local
```

#### with pipx :

```bash
$> pipx install gitsage-local
```

## Usage

```bash
$> gitsage <command> <options>
```

### Commands

    help                   Show this help message
    commit                 Generate a commit message based on the staged changes
    version/-v/--version   Show the version of GitSage

### Options

    --copy            Copy the output to the clipboard

## Configuration

The default configuration file is located at `~/.config/gitsage/config.toml`. If the file does not exist, it will be created with default values when you run the tool for the first time.

### Default Configuration :

```toml
model = "qwen3:8b"
prompt = """You generate Git commit messages.

Analyze the following staged git diff.

Return ONLY a single Conventional Commit message.
Format:
type(scope): description

Rules:
- Use feat, fix, refactor, docs, test, chore, or perf
- Keep the description concise
- Use imperative mood
- Do not invent changes
- Do not include markdown

"""
ollama_url = "http://localhost:11434"
exclude = ["*.lock", "package-lock.json", "pnpm-lock.yaml", "*.min.js", "*.min.css", "*.map"]
```

`exclude` lists glob patterns of files left out of the diff sent to the model (matched at any depth), which keeps lockfiles and generated files from filling the context. If the key is missing, the default list above is used.

You can modify the `model`, `prompt`, `ollama_url`, and `exclude` values in the configuration file to customize the behavior of GitSage according to your needs.
