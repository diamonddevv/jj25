import sys
import platform

IN_BROWSER: bool = sys.platform == 'enscripten'
IS_WASM: bool = 'wasm' in platform.machine()

TITLE: str = "jj25"
VERSION: str = "1.0.0"
AUTHOR: str = "DiamondDev"
PACKAGE: str = "dev.diamond.jj25"

CANVAS_DIMS: tuple[int, int] = (1280, 720)
WINDOW_DIMS: tuple[int, int] = (1280, 720)
TARGET_FRAMERATE: int = 0