# Chess

A basic Chess implementation using PyGame.

## Prerequisites

- Python 3.13 (managed via pyenv)
- Poetry (for dependency management)

## Setup

### 1. Install pyenv (Python version manager)

```bash
brew install pyenv
```

Add pyenv to your shell configuration (`~/.zshrc` for zsh or `~/.bash_profile` for bash):

```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Restart your terminal or run `source ~/.zshrc` to apply the changes.

### 2. Install Python 3.13

```bash
pyenv install 3.13.9
```

### 3. Set Python version for this project

The project includes a `.python-version` file that automatically activates Python 3.13.9 when you navigate to this directory (if pyenv is configured).

To manually set it:

```bash
pyenv local 3.13.9
```

### 4. Install dependencies

```bash
poetry env use $(pyenv which python)
poetry install
```

## Running the Application

```bash
poetry run python main.py
```

## Why pyenv?

This project uses Python 3.13.9 because pygame 2.6.1 doesn't have pre-built wheels for Python 3.14 yet. Using pyenv ensures everyone is on the same Python version and avoids compilation issues.
