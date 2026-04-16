#!/usr/bin/env python3
import os
import sys
import subprocess

# Install requirements if needed
def check_requirements():
    try:
        import blessed
    except ImportError:
        print("Installing requirements...")
        subprocess.call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "blessed",
            "psutil"
        ])

check_requirements()

from desktop import Desktop
import blessed

def main():
    term = blessed.Terminal()
    desktop = Desktop(term)
    try:
        desktop.run()
    except KeyboardInterrupt:
        print(term.clear)
        print("Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()