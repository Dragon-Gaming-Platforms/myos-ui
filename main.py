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

    def draw_background(self):
        t = self.term
        # Fill background with a pattern
        for y in range(1, t.height - 1):
            for x in range(0, t.width):
                # Create a dot grid pattern
                if y % 4 == 0 and x % 8 == 0:
                    print(
                        t.move(y, x) +
                        t.color_rgb(40, 40, 60) +
                        "+" +
                        t.normal,
                        end=""
                    )
                else:
                    print(
                        t.move(y, x) +
                        t.on_color_rgb(20, 20, 40) +
                        " " +
                        t.normal,
                        end=""
                    )

    def draw_topbar(self):
        t = self.term
        time = datetime.datetime.now().strftime("%H:%M:%S")
        date = datetime.datetime.now().strftime("%a %d %b %Y")
        width = t.width
        username = self.user.get_username()
        os_name = "DragonOS"

        # Full top bar background
        print(
            t.move(0, 0) +
            t.on_color_rgb(15, 15, 35) +
            " " * width +
            t.normal,
            end=""
        )

        # Left side - OS name with accent
        print(
            t.move(0, 0) +
            t.on_color_rgb(80, 0, 200) +
            t.color_rgb(255, 255, 255) +
            t.bold +
            f"  {os_name}  " +
            t.normal,
            end=""
        )

        # Middle - username
        user_text = f"  logged in as {username}  "
        print(
            t.move(0, 12) +
            t.on_color_rgb(15, 15, 35) +
            t.color_rgb(150, 150, 255) +
            user_text +
            t.normal,
            end=""
        )

        # Right side - date and time
        datetime_text = f"  {date}  {time}  "
        print(
            t.move(0, width - len(datetime_text)) +
            t.on_color_rgb(15, 15, 35) +
            t.color_rgb(200, 200, 255) +
            datetime_text +
            t.normal,
            end=""
        )

    def draw_bottombar(self):
        t = self.term
        width = t.width
        notif = self.notifications.get_latest()

        # Full bottom bar background
        print(
            t.move(t.height - 1, 0) +
            t.on_color_rgb(15, 15, 35) +
            " " * width +
            t.normal,
            end=""
        )

        # Start button
        print(
            t.move(t.height - 1, 0) +
            t.on_color_rgb(80, 0, 200) +
            t.color_rgb(255, 255, 255) +
            t.bold +
            "  MENU  " +
            t.normal,
            end=""
        )

        # Controls hint
        controls = "  ENTER:Open   ARROWS:Navigate   S:Menu   Q:Quit  "
        print(
            t.move(t.height - 1, 9) +
            t.on_color_rgb(15, 15, 35) +
            t.color_rgb(150, 150, 255) +
            controls +
            t.normal,
            end=""
        )

        # Notification on right
        print(
            t.move(t.height - 1, width - len(notif) - 2) +
            t.on_color_rgb(15, 15, 35) +
            t.color_rgb(100, 255, 100) +
            f" {notif} " +
            t.normal,
            end=""
        )

    def draw_icons(self):
        t = self.term
        icons_per_row = 3
        icon_width = 18
        icon_height = 6
        start_y = 3
        # Center icons on screen
        total_width = icons_per_row * icon_width
        start_x = (t.width - total_width) // 2

        for i, app in enumerate(self.apps):
            row = i // icons_per_row
            col = i % icons_per_row
            y = start_y + (row * icon_height)
            x = start_x + (col * icon_width)

            if i == self.selected:
                # Selected style - bright purple
                bg = t.on_color_rgb(80, 0, 200)
                fg = t.color_rgb(255, 255, 255)
                border = t.color_rgb(255, 255, 255)
            else:
                # Normal style - dark with subtle border
                bg = t.on_color_rgb(30, 30, 60)
                fg = t.color_rgb(200, 200, 255)
                border = t.color_rgb(80, 80, 150)

            # Draw icon box
            # Top border
            print(
                t.move(y, x) +
                bg + border +
                "+" + "-" * 14 + "+" +
                t.normal,
                end=""
            )
            # Icon row
            print(
                t.move(y + 1, x) +
                bg + border + "|" +
                fg + t.bold +
                f"  [{app['icon']}]        " +
                border + "|" +
                t.normal,
                end=""
            )
            # Empty row
            print(
                t.move(y + 2, x) +
                bg + border + "|" +
                " " * 14 +
                border + "|" +
                t.normal,
                end=""
            )
            # Name row
            name = app['name'][:12].center(14)
            print(
                t.move(y + 3, x) +
                bg + border + "|" +
                fg +
                name +
                border + "|" +
                t.normal,
                end=""
            )
            # Description row
            desc = app['description'][:12].center(14)
            print(
                t.move(y + 4, x) +
                bg + border + "|" +
                t.color_rgb(150, 150, 200) +
                desc +
                border + "|" +
                t.normal,
                end=""
            )
            # Bottom border
            print(
                t.move(y + 5, x) +
                bg + border +
                "+" + "-" * 14 + "+" +
                t.normal,
                end=""
            )

    def draw_start_menu(self):
        t = self.term
        if not self.start_menu_open:
            return

        menu_width = 32
        menu_height = len(self.apps) + 5
        start_x = 0
        start_y = t.height - menu_height - 1

        # Shadow effect
        for y in range(menu_height):
            print(
                t.move(start_y + y, start_x) +
                t.on_color_rgb(10, 10, 25) +
                " " * menu_width +
                t.normal,
                end=""
            )

        # Title bar
        print(
            t.move(start_y, start_x) +
            t.on_color_rgb(80, 0, 200) +
            t.color_rgb(255, 255, 255) +
            t.bold +
            f"  DragonOS Menu" +
            " " * (menu_width - 16) +
            t.normal,
            end=""
        )

        # Separator
        print(
            t.move(start_y + 1, start_x) +
            t.on_color_rgb(10, 10, 25) +
            t.color_rgb(80, 0, 200) +
            "=" * menu_width +
            t.normal,
            end=""
        )

        # Apps list
        for i, app in enumerate(self.apps):
            y = start_y + 2 + i
            if i == self.taskbar_selected:
                bg = t.on_color_rgb(80, 0, 200)
                fg = t.color_rgb(255, 255, 255)
            else:
                bg = t.on_color_rgb(10, 10, 25)
                fg = t.color_rgb(180, 180, 255)

            print(
                t.move(y, start_x) +
                bg + fg +
                f"  {app['icon']}  {app['name']:<20}  " +
                t.normal,
                end=""
            )

        # Bottom separator
        print(
            t.move(start_y + menu_height - 2, start_x) +
            t.on_color_rgb(10, 10, 25) +
            t.color_rgb(80, 0, 200) +
            "=" * menu_width +
            t.normal,
            end=""
        )

        # Version info
        print(
            t.move(start_y + menu_height - 1, start_x) +
            t.on_color_rgb(10, 10, 25) +
            t.color_rgb(100, 100, 150) +
            f"  DragonOS v1.0" +
            " " * (menu_width - 15) +
            t.normal,
            end=""
        )

    def draw(self):
        t = self.term
        print(t.home, end="")
        self.draw_background()
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
        print(t.clear + t.normal)
        print(
            t.on_color_rgb(15, 15, 35) +
            t.color_rgb(255, 255, 255) +
            " DragonOS Terminal " +
            t.normal
        )
        print(
            t.color_rgb(150, 150, 255) +
            "Type 'exit' to return to desktop\n" +
            t.normal
        )
        os.system("/bin/bash")

    def open_files(self):
        t = self.term
        print(t.clear + t.normal)
        fm = FileManager(t, self.theme)
        fm.run()

    def open_editor(self):
        t = self.term
        print(t.clear + t.normal)
        ed = Editor(t, self.theme)
        ed.run()

    def open_installer(self):
        t = self.term
        print(t.clear + t.normal)
        ins = Installer(t, self.theme)
        ins.run()

    def open_appstore(self):
        t = self.term
        print(t.clear + t.normal)
        store = AppStore(t, self.theme)
        store.run()

    def open_settings(self):
        t = self.term
        print(t.clear + t.normal)
        st = Settings(t, self.theme, self.user)
        st.run()

    # ================================
    # Input Handling
    # ================================

    def handle_input(self, key):
        t = self.term
        icons_per_row = 3

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
        print(t.clear + t.normal)
        print("Goodbye from DragonOS!")
