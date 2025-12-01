import os

from src import consts

if __name__ == "__main__":
    os.system(f"\".venv\\Scripts\\python.exe\" -m pygbag --title {consts.TITLE} --package {consts.PACKAGE} --app_name {consts.TITLE} main.py")