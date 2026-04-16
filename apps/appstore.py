#!/usr/bin/env python3
import os
import subprocess
import sys

class AppStore:
    def __init__(self, term, theme):
        self.term = term
        self.theme = theme
        self.running = True
        self.selected = 0

        # Curated list of compatible apps
        # Add your own repos here!
        self.apps = [
            {
                "name": "Hello World Python",
                "repo": "your-username/hello-world-py",
                "description": "A simple Python hello world",
                "language": "Python"
            },
            {
                "name": "Calculator",
                "repo": "your-username/calculator",
                "description": "Terminal calculator app",
                "language": "Python"
            },
            # Add more curated apps here!
        ]

    def draw(self):
        t = self.term
        print(t.clear, end="")

        # Header
        print(
            t.move(0, 0) +
            self.theme.topbar +
            " MyOS App Store " +
            " " * (t.width - 16) +
            t.normal
        )

        # App list
        for i, app in enumerate(self.apps):
            y = 2 + (i * 3)

            if i == self.selected:
                style = self.theme.selected_icon
            else:
                style = self.theme.menu

            print(
                t.move(y, 0) +
                style +
                f" {app['name']:<30} [{app['language']}] " +
                t.normal
            )
            print(
                t.move(y + 1, 0) +
                self.theme.menu +
                f"   {app['description']:<{t.width - 4}} " +
                t.normal
            )

        # Instructions
        print(
            t.move(t.height - 1, 0) +
            self.theme.bottombar +
            " [ENTER] Install  [ARROWS] Navigate  [Q] Back " +
            " " * (t.width - 48) +
            t.normal
        )
        sys.stdout.flush()

    def handle_input(self, key):
        t = self.term

        if key.code == t.KEY_UP:
            self.selected = max(0, self.selected - 1)

        elif key.code == t.KEY_DOWN:
            self.selected = min(
                len(self.apps) - 1,
                self.selected + 1
            )

        elif key == '\n' or key.code == t.KEY_ENTER:
            app = self.apps[self.selected]
            print(t.clear + t.normal)
            print(f"Installing {app['name']}...")
            subprocess.call(["install", app["repo"]])
            input("\nPress Enter to continue...")

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