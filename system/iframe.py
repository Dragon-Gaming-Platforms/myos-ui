#!/usr/bin/env python3
import json
import os
import subprocess

class IframeBridge:
    def __init__(self):
        self.bridge_file = "/tmp/iframe_bridge.json"

    def open_app(self, url, title="App"):
        """Open a URL in the browser iFrame"""
        data = {
            "action": "open",
            "url": url,
            "title": title
        }
        with open(self.bridge_file, "w") as f:
            json.dump(data, f)
        print(f"Opening {title} in app viewer...")

    def open_github_html(self, username, repo, file, title=None):
        """Open a single HTML file from GitHub"""
        url = (
            f"https://raw.githubusercontent.com/"
            f"{username}/{repo}/main/{file}"
        )
        self.open_app(url, title or f"{username}/{repo}")

    def close_app(self):
        """Close the iFrame"""
        data = {"action": "close"}
        with open(self.bridge_file, "w") as f:
            json.dump(data, f)
        print("App viewer closed")

    def open_from_repo(self, repo):
        """
        Try to find and open an HTML file
        from an installed repo
        """
        install_dir = f"/home/user/apps/{repo}"

        # Look for HTML files
        html_files = []
        for f in os.listdir(install_dir):
            if f.endswith(".html"):
                html_files.append(f)

        if html_files:
            # Prefer index.html
            if "index.html" in html_files:
                file = "index.html"
            else:
                file = html_files[0]

            username, repo_name = repo.split("/")
            self.open_github_html(
                username,
                repo_name,
                file,
                repo_name
            )
            return True
        return False