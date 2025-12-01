# (C) DiamondDev. Donate to Jingle Jam!
import pygame

from src import window
from src.game import game



if __name__ == "__main__":
    pygame.init()

    wnd = window.Window(game.GameScene)
    wnd.init_resources()
    wnd.start()
    
    