import os
import subprocess
import sys
from foundry.menu.menu import Menu
from foundry.logger.logger import logger

from foundry.version import  __version__

class PublishMenu(Menu):
    """
    Menu for building and publishing the package.
    """

    
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
        from foundry.version import __version__
        import yaml
        import re
        from datetime import datetime, timezone

        logger.d(f"🔧 Building package for version {__version__}...")

        # === Update pyproject.toml ===
        pyproject_path = os.path.join(self.repo_root, "pyproject.toml")
        with open(pyproject_path, "r", encoding="utf-8") as f:
            content = f.read()
        updated = re.sub(
            r'(version\s*=\s*["\'])(.+?)(["\'])',
            lambda m: f'{m.group(1)}{__version__}{m.group(3)}',
            content,
            count=1
        )
        with open(pyproject_path, "w", encoding="utf-8") as f:
            f.write(updated)
        logger.d(f"✔️ pyproject.toml updated to version {__version__}")

        # === Update version.py ===
        version_path = os.path.join(self.repo_root, "foundry", "version.py")
        changelog_path = os.path.join(self.repo_root,  "changelogs", f"v{__version__}.yaml")

        with open(changelog_path, "r", encoding="utf-8") as f:
            changelog = yaml.safe_load(f)
        modified_date = changelog.get("date", "UNKNOWN")
        timestamp = datetime.now(timezone.utc).astimezone().isoformat()

        with open(version_path, "r", encoding="utf-8") as f:
            version_code = f.read()
        version_code = re.sub(r'__modified__\s*=\s*".+?"', f'__modified__ = "{modified_date}"', version_code)
        version_code = re.sub(r'__timestamp__\s*=\s*".+?"', f'__timestamp__ = "{timestamp}"', version_code)
        with open(version_path, "w", encoding="utf-8") as f:
            f.write(version_code)
        logger.d(f"✔️ version.py updated with modified={modified_date} and timestamp={timestamp}")

        # === Build the package ===
        subprocess.run([sys.executable, "-m", "build"])

        if not os.path.exists(self.dist_path) or not os.listdir(self.dist_path):
            logger.w("❌ Build failed or produced no output.")
        else:
            logger.i("✔️ Build complete.")
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
        logger.d(f"Using PyPI token from {token_path}:{token[:15]}****")
        subprocess.run([
            sys.executable, "-m", "twine", "upload", "dist/*",
            "--username", "__token__",
            "--password", token
        ])
        input("Press Enter to continue...")

    import re

    def update_pyproject_version(pyproject_path="pyproject.toml"):
        with open(pyproject_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_version = __version__

        updated = re.sub(
            r'(version\s*=\s*["\'])(.+?)(["\'])',
            lambda m: f'{m.group(1)}{new_version}{m.group(3)}',
            content,
            count=1
        )

        with open(pyproject_path, "w", encoding="utf-8") as f:
            f.write(updated)

        print(f"✔️ pyproject.toml updated to version {new_version}")


if __name__ == "__main__":
    menu = PublishMenu()
menu.launch()