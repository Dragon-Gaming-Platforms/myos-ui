#!/usr/bin/env python3
import os
import json

class UserSystem:
    def __init__(self):
        self.config_file = "/home/user/.myos_user"
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        return {"username": "user"}

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f)

    def get_username(self):
        return self.config.get("username", "user")

    def set_username(self, username):
        self.config["username"] = username
        self.save_config()