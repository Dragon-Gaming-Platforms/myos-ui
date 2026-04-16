#!/usr/bin/env python3
import blessed
import datetime
import os
import sys
from apps.terminal import Terminal
from apps.files import FileManager
from apps.editor import Editor
from apps.installer import Installer
from apps.settings import Settings
from apps.appstore import AppStore
from system.theme import Theme
from system.notify import NotificationSystem
from system.user import UserSystem

class Desktop:
    def __init__(self, term):
        self.term = term
        self.running = True
        self.theme = Theme()
        self.notifications = NotificationSystem()
        self.user = UserSystem()
        self.start_menu_open = False
        self.selected = 0
        self.taskbar_selected = 0

        # Desktop Apps
        self.apps = [
            {
                "name": "Terminal",
                "icon": ">_",
                "description": "Open a terminal",
                "action": self.open_terminal
            },
            {
                "name": "Files",
                "icon": "[]",
                "description": "Browse files",
                "action": self.open_files
            },
            {
                "name": "Editor",
                "icon": "ED",
                "description": "Edit text files",
                "action": self.open_editor
            },
            {
                "name": "Install",
                "icon": "IN",
                "description": "Install from GitHub",
                "action": self.open_installer
            },
            {
                "name": "App Store",
                "icon": "AS",
                "description": "Browse curated apps",
                "action": self.open_appstore
            },
            {
                "name": "Settings",
                "icon": "ST",
                "description": "System settings",
                "action": self.open_settings
            },
        ]

    # ================================
    # Drawing Methods
    # ================================

    def draw_topbar(self):
        t = self.term
        time = datetime.datetime.now().strftime("%H:%M:%S")
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        width = t.width
        username = self.user.get_username()
        os_name = "MyOS"

        bar = (
            t.move(0, 0) +
            self.theme.topbar +
            f" {os_name} " +
            t.normal +
            self.theme.topbar +
            " | " +
            f" {username} " +
            " " * (width - len(os_name) - len(username) - len(time) - len(date) - 10) +
            date +
            " " +
            time +
            " " +
            t.normal
        )
        print(bar, end="")

    def draw_bottombar(self):
        t = self.term
        width = t.width
        notif = self.notifications.get_latest()

        bar = (
            t.move(t.height - 1, 0) +
            self.theme.bottombar +
            " [ENTER] Open  " +
            " [ARROWS] Navigate  " +
            " [S] Start Menu  " +
            " [Q] Quit  " +
            " " * (width - 50 - len(notif)) +
            notif +
            " " +
            t.normal
        )
        print(bar, end="")

    def draw_desktop(self):
        t = self.term
        # Draw desktop background
        for y in range(1, t.height - 1):
            print(
                t.move(y, 0) +
                self.theme.desktop +
                " " * t.width +
                t.normal,
                end=""
            )

    def draw_icons(self):
        t = self.term
        start_y = 2
        start_x = 3
        icons_per_row = 4
        icon_width = 12
        icon_height = 4

        for i, app in enumerate(self.apps):
            row = i // icons_per_row
            col = i % icons_per_row
            y = start_y + (row * icon_height)
            x = start_x + (col * icon_width)

            if i == self.selected:
                style = self.theme.selected_icon
            else:
                style = self.theme.icon

            # Draw icon box
            print(t.move(y, x) + style + 
                  f" {app['icon']}         " + t.normal)
            print(t.move(y + 1, x) + style + 
                  f"            " + t.normal)
            print(t.move(y + 2, x) + style + 
                  f" {app['name'][:10]:<10} " + t.normal)

    def draw_start_menu(self):
        t = self.term
        if not self.start_menu_open:
            return

        menu_width = 30
        menu_height = len(self.apps) + 4
        start_x = 0
        start_y = t.height - menu_height - 1

        # Draw menu background
        for y in range(menu_height):
            print(
                t.move(start_y + y, start_x) +
                self.theme.menu +
                " " * menu_width +
                t.normal,
                end=""
            )

        # Draw title
        print(
            t.move(start_y, start_x) +
            self.theme.menu_title +
            " MyOS Start Menu" +
            " " * (menu_width - 17) +
            t.normal,
            end=""
        )

        # Draw separator
        print(
            t.move(start_y + 1, start_x) +
            self.theme.menu +
            "-" * menu_width +
            t.normal,
            end=""
        )

        # Draw apps
        for i, app in enumerate(self.apps):
            y = start_y + 2 + i
            if i == self.taskbar_selected:
                style = self.theme.menu_selected
            else:
                style = self.theme.menu

            print(
                t.move(y, start_x) +
                style +
                f" {app['icon']} {app['name']:<20} " +
                t.normal,
                end=""
            )

        # Draw bottom separator
        print(
            t.move(start_y + menu_height - 1, start_x) +
            self.theme.menu +
            "-" * menu_width +
            t.normal,
            end=""
        )

    def draw(self):
        t = self.term
        print(t.home, end="")
        self.draw_desktop()
        self.draw_topbar()
        self.draw_icons()
        self.draw_bottombar()
        if self.start_menu_open:
            self.draw_start_menu()
        sys.stdout.flush()

    # ================================
    # App Launchers
    # ================================

    def open_terminal(self):
        t = self.term
        print(t.clear)
        print(t.normal)
        print("=== Terminal ===")
        print("Type 'exit' to return to desktop")
        print("")
        os.system("/bin/bash")

    def open_files(self):
        t = self.term
        print(t.clear)
        print(t.normal)
        fm = FileManager(t, self.theme)
        fm.run()

    def open_editor(self):
        t = self.term
        print(t.clear)
        print(t.normal)
        ed = Editor(t, self.theme)
        ed.run()

    def open_installer(self):
        t = self.term
        print(t.clear)
        print(t.normal)
        ins = Installer(t, self.theme)
        ins.run()

    def open_appstore(self):
        t = self.term
        print(t.clear)
        print(t.normal)
        store = AppStore(t, self.theme)
        store.run()

    def open_settings(self):
        t = self.term
        print(t.clear)
        print(t.normal)
        st = Settings(t, self.theme, self.user)
        st.run()

    # ================================
    # Input Handling
    # ================================

    def handle_input(self, key):
        t = self.term
        icons_per_row = 4

        if self.start_menu_open:
            if key.code == t.KEY_UP:
                self.taskbar_selected = max(
                    0, self.taskbar_selected - 1
                )
            elif key.code == t.KEY_DOWN:
                self.taskbar_selected = min(
                    len(self.apps) - 1,
                    self.taskbar_selected + 1
                )
            elif key == '\n' or key.code == t.KEY_ENTER:
                self.start_menu_open = False
                self.apps[self.taskbar_selected]["action"]()
            elif key == 's' or key == 'S':
                self.start_menu_open = False
            elif key == 'q' or key == 'Q':
                self.start_menu_open = False
                self.running = False
        else:
            if key.code == t.KEY_UP:
                self.selected = max(
                    0, self.selected - icons_per_row
                )
            elif key.code == t.KEY_DOWN:
                self.selected = min(
                    len(self.apps) - 1,
                    self.selected + icons_per_row
                )
            elif key.code == t.KEY_LEFT:
                self.selected = max(0, self.selected - 1)
            elif key.code == t.KEY_RIGHT:
                self.selected = min(
                    len(self.apps) - 1,
                    self.selected + 1
                )
            elif key == '\n' or key.code == t.KEY_ENTER:
                self.apps[self.selected]["action"]()
            elif key == 's' or key == 'S':
                self.start_menu_open = True
                self.taskbar_selected = 0
            elif key == 'q' or key == 'Q':
                self.running = False

    # ================================
    # Main Loop
    # ================================

    def run(self):
        t = self.term
        with t.fullscreen(), t.cbreak(), t.hidden_cursor():
            while self.running:
                self.draw()
                key = t.inkey(timeout=0.5)
                if key:
                    self.handle_input(key)
        print(t.clear)
        print(t.normal)
        print("Goodbye!")