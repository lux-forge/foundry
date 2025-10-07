#!/usr/bin/env python3

# git_menu.py
# Author: Luxforge
# Host menu for Git utilities and wiki tooling

from foundry.menu.menu import Menu
from foundry.utils.paths import PathLoader


class GitMenu(Menu):
    """
    Git menu for managing Git-related tasks.
    """

    MENU_META = {
        "name": "GitMenu",
        "desc": "Menu selection items for git - push, pull, rebranch etc",
        "keys": ("git", "g"),
    }

    menu_name = "Git Menu"
    options = {
        "1": ("Trial request_path()", "trial_request_path"),
        # Future options:
        # "2": ("Run breadcrumbs injector", "run_breadcrumbs"),
        # "3": ("Emit changelog", "emit_changelog")
    }

    def trial_request_path(self):
        path = PathLoader.request_path("Enter a directory to trial path resolution")
        self._Menu__print(f"[+] Resolved path: {path}", colour="green")
        input("Press Enter to continue...")
