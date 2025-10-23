# paths.py
# Author: Luxforge
# Centralized path resolver for repo-rooted assets and directories. Offers a means of getting a path too

from asyncio.log import logger
import os
from pathlib import Path
import sys

class PathLoader:
    def __init__(self):
        import os
        # Determine the foundry root directory - within the foundry folder, 1 level down from the root
        self.root = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        print(f"[+] Foundry root resolved to: {self.root}")

        # Search the repo root for dirs and create properties
        for dir_name in os.listdir(self.root):
            dir_path = self.root / dir_name
            if os.path.isdir(dir_path):

                # Return the path as a Path object
                setattr(self, dir_name, Path(dir_path))
        
    # Test the paths
    def print_paths(self):
        paths = self.__dict__
        print("Resolved Paths:")

        # Retrieve the properties dynamically
        for key, value in paths.items():
            if not key.startswith("_") and not callable(getattr(self, key)):
                print(f"  {key}: {value}")

    @staticmethod
    def request_path(prompt: str = "Enter path to target directory", default: str = None) -> str:
        """
        Prompts the user for a valid directory path.
        - Accepts a custom prompt
        - Defaults to current working directory if none provided
        - Re-prompts if invalid
        - Exits cleanly on 'X' or 'EXIT'
        """
        default = default or os.getcwd()

        print(f"\n{prompt} [Default: {default}]")
        user_input = input(">>> ").strip()

        # Exit triggers
        if user_input.upper() in ["X", "EXIT", "QUIT", "Q"]:
            print("[+] Exiting path prompt.")
            sys.exit(0)

        # Use default if empty
        path = user_input or default

        # Validate
        if os.path.isdir(path):
            # if logger not loaded, just print
            try:
                logger.info(f"Validated path: {path}")
            except ImportError:
                print(f"Validated path: {path}")
            return path
        else:
            try:
                logger.error(f"Invalid path: {path}")
            except ImportError:
                print(f"[!] '{path}' is not a valid directory.")
            return request_path(prompt=prompt, default=default)


def request_path(prompt: str = "Enter path to target directory", default: str = None) -> str:
    """
    Prompts the user for a valid directory path.
    - Accepts a custom prompt
    - Defaults to current working directory if none provided
    - Re-prompts if invalid
    - Exits cleanly on 'X' or 'EXIT'
    """
    default = default or os.getcwd()

    print(f"\n{prompt} [Default: {default}]")
    user_input = input(">>> ").strip()

    # Exit triggers
    if user_input.upper() in ["X", "EXIT", "QUIT", "Q"]:
        print("[+] Exiting path prompt.")
        sys.exit(0)

    # Use default if empty
    path = user_input or default

    # Validate
    if os.path.isdir(path):
        logger.info(f"Validated path: {path}")
        return path
    else:
        print(f"[!] '{path}' is not a valid directory.")
        return request_path(prompt=prompt, default=default)

paths = PathLoader()
if __name__ == "__main__":
    paths.print_paths()