# (C) DiamondDev. Donate to Jingle Jam!
import pygame
import asyncio

from src import window
from src.game import game
from src.menu import mainmenu



if __name__ == "__main__":
    pygame.init()

    wnd = window.Window(mainmenu.MainMenu)
    wnd.init_resources()
    
    asyncio.run(wnd.start())
    
    