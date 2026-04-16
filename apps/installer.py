#!/usr/bin/env python3
import os
import subprocess
import sys

class Installer:
    def __init__(self, term, theme):
        self.term = term
        self.theme = theme
        self.running = True
        self.installed = self.get_installed()

    def get_installed(self):
        install_dir = "/home/user/apps"
        installed = []
        if os.path.exists(install_dir):
            for user in os.listdir(install_dir):
                user_dir = os.path.join(install_dir, user)
                if os.path.isdir(user_dir):
                    for repo in os.listdir(user_dir):
                        installed.append(f"{user}/{repo}")
        return installed

    def draw(self):
        t = self.term
        print(t.clear, end="")

        # Header
        print(
            t.move(0, 0) +
            self.theme.topbar +
            " GitHub Installer " +
            " " * (t.width - 18) +
            t.normal
        )

        # Installed apps
        print(t.move(2, 0) + " Installed Apps:")
        if self.installed:
            for i, app in enumerate(self.installed):
                print(t.move(3 + i, 2) + f"- {app}")
        else:
            print(t.move(3, 2) + "No apps installed yet")

        # Instructions
        print(
            t.move(t.height - 1, 0) +
            self.theme.bottombar +
            " [I] Install  [R] Remove  [Q] Back " +
            " " * (t.width - 36) +
            t.normal
        )
        sys.stdout.flush()

    def install_app(self):
        t = self.term
        print(t.clear + t.normal)
        print("=== Install from GitHub ===\n")
        print("Enter repository (username/repo):")
        repo = input("> ").strip()

        if repo:
            print(f"\nInstalling {repo}...")
            result = subprocess.call(["install", repo])
            if result == 0:
                print(f"\n{repo} installed successfully!")
            else:
                print(f"\nFailed to install {repo}")
            input("\nPress Enter to continue...")
            self.installed = self.get_installed()

    def remove_app(self):
        t = self.term
        print(t.clear + t.normal)
        print("=== Remove App ===\n")
        print("Enter repository to remove (username/repo):")
        repo = input("> ").strip()

        if repo:
            app_dir = f"/home/user/apps/{repo}"
            if os.path.exists(app_dir):
                subprocess.call(["rm", "-rf", app_dir])
                print(f"\n{repo} removed!")
            else:
                print(f"\n{repo} not found!")
            input("\nPress Enter to continue...")
            self.installed = self.get_installed()

    def handle_input(self, key):
        if key == 'i' or key == 'I':
            self.install_app()
        elif key == 'r' or key == 'R':
            self.remove_app()
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