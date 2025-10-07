#!/usr/bin/env python3

# breadcrumbs.py
# Author: Luxforge
# Injects Rasputin-style NAVIGATION breadcrumbs into markdown files

import os
from foundry.utils.logger import logger
from foundry.utils.files import find_markdown_files, inject_line
from foundry.menu.menu import Menu
from foundry.utils.paths import PathLoader


__description__ = "Inject Rasputin-style NAVIGATION breadcrumbs into markdown files"


class BreadcrumbMenu(Menu):
    menu_name = "Breadcrumb Injector"
    options = {
        "1": ("Inject breadcrumbs into all .md files", "inject_all"),
    }

    def inject_all(self):
        """
        Injects breadcrumbs into all markdown files using a user-provided source directory.
        """

        # Use the path loader to get the config directory - it handles validation
        source_dir = PathLoader.request_path("Enter wiki directory")

        inject_breadcrumbs(source_dir)
        logger.i("Breadcrumb injection complete.")
        input("Press Enter to continue...")


def generate_breadcrumb(path: str, root: str = None) -> str:
    """
    Generates a NAVIGATION breadcrumb line for a given markdown file path.
    """
    
    rel_path = os.path.relpath(path, root) if root else path
    parts = rel_path.replace("\\", "/").split("/")
    breadcrumb = " / ".join(parts)

    logger.d(f"Generated breadcrumb for {path}: {breadcrumb}")
    return f"<!-- NAVIGATION: {breadcrumb} -->"


def inject_breadcrumbs(source_dir: str):
    """
    Injects NAVIGATION breadcrumbs into all markdown files under source_dir.
    """
    logger.d(f"Injecting breadcrumbs into markdown files in: {source_dir}")
    md_files = find_markdown_files(source_dir)

    for path in md_files:
        breadcrumb = generate_breadcrumb(path, root=source_dir)
        inject_line(path, breadcrumb)
        logger.d(f"Injected breadcrumb into {path}")
