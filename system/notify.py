#!/usr/bin/env python3
import datetime

class NotificationSystem:
    def __init__(self):
        self.notifications = []

    def add(self, message):
        time = datetime.datetime.now().strftime("%H:%M")
        self.notifications.append(f"[{time}] {message}")

    def get_latest(self):
        if self.notifications:
            return self.notifications[-1]
        return "Welcome to MyOS!"

    def get_all(self):
        return self.notifications