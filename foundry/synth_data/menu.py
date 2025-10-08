# /usr/bin/env python3

# menu.py
# Author: Luxforge
# Synth Data Menu

from menu import Menu
from foundry.utils.logger import logger
from synth_data import SynthData
from foundry.utils.pathloader import paths

class SynthDataMenu(Menu):
    """
    Interactive CLI menu for managing synthetic data generation tasks.
    """

    MENU_META = {
        "name": "SynthDataMenu",  # Display name
        "desc": "Menu for generating and managing synthetic data"  # Description
    }
    def _set_options(self):
        self.options = {
            "G": ("Generate Synthetic Data", self.generate_synthetic_data),
            "V": ("View Generated Data", self.view_generated_data),
            "C": ("Configure Data Parameters", self.configure_data_parameters),
        }
    
    def generate_synthetic_data(self):
        synth_data = SynthData()
        synth_data.generate_data()
        input("Press Enter to return to the menu...")
    
    def view_generated_data(self):
        synth_data = SynthData()
        synth_data.view_data()
        input("Press Enter to return to the menu...")

    def configure_data_parameters(self):
        synth_data = SynthData()
        synth_data.configure_parameters()
        input("Press Enter to return to the menu...")