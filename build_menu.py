import os
import subprocess
from foundry.menu.menu import Menu
from foundry.logger.logger import logger

from foundry.version import update_pyproject_version, __version__

class PublishMenu(Menu):
    """
    Menu for building and publishing the package.
    """

    MENU_META = {
        "name": "Publish Menu",
        "description": "Menu for building and publishing the package.",
    }
    def __init__(self):
        super().__init__()
        self.dist_path = os.path.join(os.getcwd(), "dist")
        self.repo_root = os.path.dirname(os.path.abspath(__file__))

    def _set_options(self):
        self.options = {
            "1": ("Clean old builds", self.clean),
            "2": ("Build package", self.build),
            "3": ("Push to PyPI", self.push)
        }
        
    def clean(self):
        logger.d("Cleaning old builds...")
        if os.path.exists(self.dist_path):
            for file in os.listdir(self.dist_path):
                os.remove(os.path.join(self.dist_path, file))
            logger.d("Dist folder cleaned.")
        else:
            logger.d("No dist folder found.")
        input("Press Enter to continue...")

    def build(self):
        logger.d(f"🔧 Building package for version {__version__}...")
        
        # Sync pyproject.toml
        update_pyproject_version()

        # Run build
        subprocess.run(["python", "-m", "build"])

        if not os.path.exists(self.dist_path) or not os.listdir(self.dist_path):
            logger.w("❌ Build failed or produced no output.")
        else:
            logger.i("✔️ Build complete. " )
            logger.d("Files in dist/:")
            for f in os.listdir(self.dist_path):
                logger.d(f"  - {f}")
        input("Press Enter to continue...")

    def push(self):
        logger.i("🚀 Pushing to PyPI...")

        token_path = os.path.join(self.repo_root, ".secrets", "pypi.token")
        if not os.path.exists(token_path):
            logger.e("❌ PyPI token file not found.")
            return

        with open(token_path, "r", encoding="utf-8") as f:
            token = f.read().strip()

        subprocess.run([
            "twine", "upload", "dist/*",
            "--username", "__token__",
            "--password", token
        ])
        input("Press Enter to continue...")

if __name__ == "__main__":
    menu = PublishMenu()
menu.launch()