import pygame

from src import util
from src import event
from src import consts
from src.render import camera
from src.render import animate
from src.render import spritesheet
from src.render import ui
from src.game import game
from src.game import pirate
from src.menu import menu
from src.menu import mainmenu


class CreditsScene(menu.MenuScene):
    TEXT: str = """
       Thank you to everyone who made this game possible!

              PROGRAMMING:        Fynn (DiamondDev)
                   DESIGN:        Fynn (DiamondDev), Euan Stables
                      ART:        Fynn (DiamondDev)
                    MUSIC:        Euan Stables

     Special Thanks to:          Made with:
            - Team impROVise        - pygame-ce 2.5.6
                                   - Python 3.14.1
                                   - Aseprite
                                   - Microsoft VSCode
                                   - JSFXR


    This game was made for the Annual Yogscast Jingle Jam.
    Since 2011, they have raised over £27M for several good causes.
    Donate at https://www.jinglejam.co.uk/.


                       From Scotland with <3!
"""

    def __init__(self, camera: camera.Camera) -> None:
        super().__init__(camera)
        camera.fill_col = 0xffffff

        self.container.add(
            ui.UiText(pygame.Vector2(consts.CANVAS_DIMS[0] / 2, 125),
                      lambda: "Credits", 3, 0x000000, centered=True, sfsans=True)
        )
        self.container.add(
            ui.UiTexture(pygame.Vector2(consts.CANVAS_DIMS[0] / 2 - 200, consts.CANVAS_DIMS[1] / 2 + 24), 'res/astrid.png', scale=2)
        )
        self.container.add(
            ui.UiText(pygame.Vector2(consts.CANVAS_DIMS[0] / 2, 530),
                      lambda: CreditsScene.TEXT, 2, 0x000000, centered=True)
        )
        
        self.container.add(
            ui.UiButton(
                pygame.Vector2(consts.CANVAS_DIMS[0] / 2, consts.CANVAS_DIMS[1] - 128),
                lambda: "Back", 4, lambda: pygame.event.post(
                    pygame.Event(event.CHANGE_SCENE, {
                        'scene': mainmenu.MainMenu
                    })
                ), 0x6a6a6a, centered=True
            )
        )

        