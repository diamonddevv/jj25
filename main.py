# (C) DiamondDev. Donate to Jingle Jam!
import pygame

from src import window
from src.game import test



if __name__ == "__main__":
    pygame.init()
    wnd = window.Window(test.TestScene)
    wnd.start()
    
    