#!/usr/bin/env python3
import os
import sys

class FileManager:
    def __init__(self, term, theme):
        self.term = term
        self.theme = theme
        self.current_dir = os.path.expanduser("~")
        self.selected = 0
        self.running = True
        self.files = []

    def get_files(self):
        try:
            files = [".."] + sorted(os.listdir(self.current_dir))
            self.files = files
        except PermissionError:
            self.files = [".."]

    def draw(self):
        t = self.term
        print(t.clear, end="")

        # Header
        print(
            t.move(0, 0) +
            self.theme.topbar +
            f" File Manager - {self.current_dir} " +
            " " * (t.width - len(self.current_dir) - 18) +
            t.normal
        )

        # Instructions
        print(
            t.move(1, 0) +
            self.theme.bottombar +
            " [ENTER] Open  [BACKSPACE] Back  [Q] Quit " +
            " " * (t.width - 43) +
            t.normal
        )

        # Files
        self.get_files()
        for i, f in enumerate(self.files[:t.height - 3]):
            y = i + 2
            path = os.path.join(self.current_dir, f)

            if os.path.isdir(path):
                prefix = "[ ] "
            else:
                prefix = "    "

            if i == self.selected:
                style = self.theme.selected_icon
            else:
                style = self.theme.menu

            print(
                t.move(y, 0) +
                style +
                f" {prefix}{f:<{t.width - 6}} " +
                t.normal
            )

        sys.stdout.flush()

    def handle_input(self, key):
        t = self.term

        if key.code == t.KEY_UP:
            self.selected = max(0, self.selected - 1)

        elif key.code == t.KEY_DOWN:
            self.selected = min(
                len(self.files) - 1,
                self.selected + 1
            )

        elif key == '\n' or key.code == t.KEY_ENTER:
            if self.files:
                selected_file = self.files[self.selected]
                path = os.path.join(
                    self.current_dir,
                    selected_file
                )
                if selected_file == "..":
                    self.current_dir = os.path.dirname(
                        self.current_dir
                    )
                    self.selected = 0
                elif os.path.isdir(path):
                    self.current_dir = path
                    self.selected = 0
                else:
                    # Open file with vim
                    import subprocess
                    subprocess.call(["vim", path])

        elif key.code == t.KEY_BACKSPACE:
            self.current_dir = os.path.dirname(
                self.current_dir
            )
            self.selected = 0

        elif key == 'q' or key == 'Q':
            self.running = False

    def run(self):
        t = self.term
        with t.cbreak(), t.hidden_cursor():
            while self.running:
                self.draw()
                key = t.inkey(timeout=0.5)
                if key:
                    self.handle_input(key)