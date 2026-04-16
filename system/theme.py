#!/usr/bin/env python3
import blessed
import os
import json

class Theme:
    def __init__(self):
        self.term = blessed.Terminal()
        self.theme_file = "/home/user/.myos_theme"
        self.current_theme = self.load_theme()
        self.apply_theme()

    def load_theme(self):
        if os.path.exists(self.theme_file):
            with open(self.theme_file, "r") as f:
                return json.load(f).get("theme", "1")
        return "1"

    def save_theme(self, theme):
        with open(self.theme_file, "w") as f:
            json.dump({"theme": theme}, f)

    def set_theme(self, theme):
        self.current_theme = theme
        self.save_theme(theme)
        self.apply_theme()

    def apply_theme(self):
        t = self.term

        if self.current_theme == "1":
            # Dark theme
            self.topbar = t.black_on_white
            self.bottombar = t.black_on_white
            self.desktop = t.normal
            self.icon = t.normal
            self.selected_icon = t.black_on_cyan
            self.menu = t.white_on_black
            self.menu_title = t.black_on_white
            self.menu_selected = t.black_on_cyan

        elif self.current_theme == "2":
            # Light theme
            self.topbar = t.white_on_black
            self.bottombar = t.white_on_black
            self.desktop = t.normal
            self.icon = t.normal
            self.selected_icon = t.white_on_blue
            self.menu = t.black_on_white
            self.menu_title = t.white_on_black
            self.menu_selected = t.white_on_blue

        elif self.current_theme == "3":
            # Retro Green theme
            self.topbar = t.black_on_green
            self.bottombar = t.black_on_green
            self.desktop = t.green_on_black
            self.icon = t.green_on_black
            self.selected_icon = t.black_on_green
            self.menu = t.green_on_black
            self.menu_title = t.black_on_green
            self.menu_selected = t.black_on_green

        elif self.current_theme == "4":
            # Retro Amber theme
            self.topbar = t.black_on_yellow
            self.bottombar = t.black_on_yellow
            self.desktop = t.yellow_on_black
            self.icon = t.yellow_on_black
            self.selected_icon = t.black_on_yellow
            self.menu = t.yellow_on_black
            self.menu_title = t.black_on_yellow
            self.menu_selected = t.black_on_yellow