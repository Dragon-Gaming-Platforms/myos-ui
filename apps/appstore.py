#!/usr/bin/env python3
import os
import subprocess
import sys
import json
import urllib.request
from system.iframe import IframeBridge

class AppStore:
    def __init__(self, term, theme):
        self.term = term
        self.theme = theme
        self.running = True
        self.selected = 0
        self.bridge = IframeBridge()
        self.apps = self.load_apps()

    def load_apps(self):
        """Load apps from your GitHub appstore.json"""
        try:
            url = (
                "https://raw.githubusercontent.com/"
                "your-username/myos-ui/main/appstore.json"
            )
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read().decode())
        except Exception:
            # Fallback local list
            return [
                {
                    "name": "No internet connection",
                    "description": "Connect via Tailscale",
                    "type": "Error",
                    "html_url": None,
                    "repo": None
                }
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
            y = 2 + (i * 4)
            if y > t.height - 5:
                break

            if i == self.selected:
                style = self.theme.selected_icon
            else:
                style = self.theme.menu

            app_type = app.get("type", "Unknown")
            name = app.get("name", "Unknown")
            desc = app.get("description", "")

            print(
                t.move(y, 0) +
                style +
                f" {name:<35} [{app_type}] " +
                " " * (t.width - len(name) - len(app_type) - 10) +
                t.normal
            )
            print(
                t.move(y + 1, 0) +
                self.theme.menu +
                f"   {desc:<{t.width - 4}}" +
                t.normal
            )

            # Show available actions
            actions = []
            if app.get("html_url"):
                actions.append("[ENTER] Open in Viewer")
            if app.get("repo"):
                actions.append("[I] Install")

            print(
                t.move(y + 2, 0) +
                self.theme.menu +
                f"   {' | '.join(actions):<{t.width - 4}}" +
                t.normal
            )

        # Instructions
        print(
            t.move(t.height - 1, 0) +
            self.theme.bottombar +
            " [ENTER] Open  [I] Install  "
            "[R] Refresh  [Q] Back " +
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
            if app.get("html_url"):
                self.bridge.open_app(
                    app["html_url"],
                    app["name"]
                )
                print(t.clear + t.normal)
                print(f"Opened {app['name']} in app viewer!")
                print("Check the panel on the right")
                input("\nPress Enter to continue...")

        elif key == 'i' or key == 'I':
            app = self.apps[self.selected]
            if app.get("repo"):
                print(t.clear + t.normal)
                print(f"Installing {app['name']}...")
                subprocess.call(["install", app["repo"]])
                input("\nPress Enter to continue...")

        elif key == 'r' or key == 'R':
            print(t.clear + t.normal)
            print("Refreshing app store...")
            self.apps = self.load_apps()
            print("Done!")

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