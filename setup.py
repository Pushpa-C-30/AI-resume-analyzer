#!/usr/bin/env python3
"""
setup.py  — one-time project setup script.
Run:  python setup.py
"""
import subprocess
import sys
import os


def run(cmd, desc=""):
    print(f"\n{'─'*50}")
    if desc:
        print(f"  {desc}")
    print(f"  $ {cmd}\n")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[ERROR] Command failed (exit {result.returncode})")
        sys.exit(result.returncode)


def main():
    print("=" * 50)
    print("  AI Resume Analyzer — Setup")
    print("=" * 50)

    run("pip install -r requirements.txt", "Installing Python dependencies")

    # Download NLTK data (punkt tokenizer)
    run(
        'python -c "import nltk; nltk.download(\'punkt\', quiet=True); nltk.download(\'stopwords\', quiet=True)"',
        "Downloading NLTK data"
    )

    print("\n" + "=" * 50)
    print("  Setup complete!")
    print()
    print("  To start the backend API:")
    print("    cd backend && python app.py")
    print()
    print("  Then open frontend/index.html in your browser.")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
