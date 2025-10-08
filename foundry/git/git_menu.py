#!/usr/bin/env python3

# git_menu.py
# Author: Luxforge
# Host menu for Git utilities and wiki tooling

from foundry.menu.menu import Menu
from foundry.utils.paths import PathLoader
from foundry.utils.logger import logger


class GitMenu(Menu):
    """
    Git menu for managing Git-related tasks.
    """

    MENU_META = {
        "name": "GitMenu",
        "desc": "Menu selection items for git - push, pull, rebranch etc"
    }

    def _set_options(self):
        self.options = {
            "1": ("Clone repo", self.clone_repo),
            "2": ("Push changes", self.push_changes),
            "3": ("View status", self.view_status),
            "4": ("Trial request path", self.trial_request_path),

        }

    def clone_repo(self):
        logger.warning("Clone repo functionality is not yet implemented.")
        input("Press Enter to return to the menu...")

    def push_changes(self):
        logger.warning("Push changes functionality is not yet implemented.")
        input("Press Enter to return to the menu...")

    def view_status(self):
        logger.warning("View status functionality is not yet implemented.")
        input("Press Enter to return to the menu...")

    def trial_request_path(self):
        path = PathLoader.request_path("Enter a directory to trial path resolution")
        self._Menu__print(f"[+] Resolved path: {path}", colour="green")
        input("Press Enter to continue...")
