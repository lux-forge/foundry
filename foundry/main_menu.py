#!/usr/bin/env python3

# main_menu.py
# Author: Luxforge
# Main menu launcher for Luxforge tools


from menu.menu import Menu
# Load the other classes and functions

class MainMenu(Menu):
    """
    Interactive CLI menu for management tasks.
    """
    options = {
        "D": ("Docker", "load_docker_menu"),
        "P": ("Load Paths", "load_paths_menu"),
        "U": ("User Management", "load_user_menu"),
        "G": ("Games", "load_games_menu"),
        "1": ("Git Utilities", "load_git_menu")
    }
    menu_name = "Main Menu"
    
    def load_docker_menu(self):
        from foundry.docker.menu import DockerMenu
        DockerMenu(previous_menu=self).launch()
    
    def load_paths_menu(self):
        from foundry.utils.paths import paths
        paths.print_paths()
        input("Press Enter to return to the menu...")
    
    def load_user_menu(self):
        from foundry.users.users import UserMenu
        UserMenu(previous_menu=self).launch()
    
    def load_games_menu(self):
        from foundry.games.menu import GamesMenu
        GamesMenu(previous_menu=self).launch()

    def load_git_menu(self):
        from foundry.git.git_menu import GitMenu
        GitMenu(previous_menu=self).launch()
if __name__ == "__main__":
    menu = MainMenu()
    menu.launch()