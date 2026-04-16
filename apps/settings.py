#!/usr/bin/env python3
import os
import sys
import subprocess

class Settings:
    def __init__(self, term, theme, user):
        self.term = term
        self.theme = theme
        self.user = user
        self.running = True
        self.selected = 0
        self.options = [
            "Change Theme",
            "Change Username",
            "Change Password",
            "System Info",
            "Back"
        ]

    def draw(self):
        t = self.term
        print(t.clear, end="")

        # Header
        print(
            t.move(0, 0) +
            self.theme.topbar +
            " Settings " +
            " " * (t.width - 10) +
            t.normal
        )

        # Options
        for i, option in enumerate(self.options):
            y = 2 + i
            if i == self.selected:
                style = self.theme.selected_icon
            else:
                style = self.theme.menu

            print(
                t.move(y, 2) +
                style +
                f" {option:<30} " +
                t.normal
            )

        # Instructions
        print(
            t.move(t.height - 1, 0) +
            self.theme.bottombar +
            " [ENTER] Select  [ARROWS] Navigate  [Q] Back " +
            " " * (t.width - 47) +
            t.normal
        )
        sys.stdout.flush()

    def change_theme(self):
        print(self.term.clear + self.term.normal)
        print("=== Change Theme ===\n")
        print("Available themes:")
        print("1. Default (Dark)")
        print("2. Light")
        print("3. Retro Green")
        print("4. Retro Amber")
        choice = input("\nChoose theme (1-4): ").strip()
        self.theme.set_theme(choice)
        input("\nTheme changed! Press Enter to continue...")

    def change_username(self):
        print(self.term.clear + self.term.normal)
        print("=== Change Username ===\n")
        new_name = input("Enter new username: ").strip()
        if new_name:
            self.user.set_username(new_name)
            print(f"Username changed to {new_name}!")
        input("\nPress Enter to continue...")

    def change_password(self):
        print(self.term.clear + self.term.normal)
        print("=== Change Password ===\n")
        new_pass = input("Enter new password: ").strip()
        if new_pass:
            subprocess.call(
                f"echo 'user:{new_pass}' | chpasswd",
                shell=True
            )
            print("Password changed!")
        input("\nPress Enter to continue...")

    def system_info(self):
        print(self.term.clear + self.term.normal)
        print("=== System Info ===\n")
        os.system("uname -a")
        print("")
        os.system("df -h /")
        print("")
        os.system("free -h")
        print("")
        os.system("cat /proc/cpuinfo | grep 'model name' | head -1")
        input("\nPress Enter to continue...")

    def handle_input(self, key):
        t = self.term

        if key.code == t.KEY_UP:
            self.selected = max(0, self.selected - 1)

        elif key.code == t.KEY_DOWN:
            self.selected = min(
                len(self.options) - 1,
                self.selected + 1
            )

        elif key == '\n' or key.code == t.KEY_ENTER:
            if self.selected == 0:
                self.change_theme()
            elif self.selected == 1:
                self.change_username()
            elif self.selected == 2:
                self.change_password()
            elif self.selected == 3:
                self.system_info()
            elif self.selected == 4:
                self.running = False

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