#!/usr/bin/env python3
import os
import subprocess

class Editor:
    def __init__(self, term, theme):
        self.term = term
        self.theme = theme

    def run(self):
        t = self.term
        print(t.clear + t.normal)
        print("=== MyOS Editor ===\n")
        print("Enter filename to edit (or press Enter for new file):")
        filename = input("> ").strip()

        if filename:
            subprocess.call(["vim", filename])
        else:
            subprocess.call(["vim"])