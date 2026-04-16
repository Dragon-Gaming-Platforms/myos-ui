#!/usr/bin/env python3
import os

class Terminal:
    def __init__(self, term, theme):
        self.term = term
        self.theme = theme

    def run(self):
        t = self.term
        print(t.clear + t.normal)
        print("=== MyOS Terminal ===")
        print("Type 'exit' to return to desktop\n")
        os.system("/bin/bash")