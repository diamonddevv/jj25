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


class WinScene(menu.MenuScene):

    def __init__(self, camera: camera.Camera) -> None:
        super().__init__(camera)
        camera.fill_col = 0xffffff

        self.container.add(
            ui.UiText(pygame.Vector2(consts.CANVAS_DIMS[0] / 2, 125),
                      lambda: "winner", 3, 0x000000, centered=True, sfsans=True)
        )
        self.container.add(
            ui.UiText(pygame.Vector2(consts.CANVAS_DIMS[0] / 2, 530),
                      lambda: "you didded it", 2, 0x000000, centered=True)
        )
        
        self.container.add(
            ui.UiButton(
                pygame.Vector2(consts.CANVAS_DIMS[0] / 2, consts.CANVAS_DIMS[1] - 128),
                lambda: "ok", 4, lambda: pygame.event.post(
                    pygame.Event(event.CHANGE_SCENE, {
                        'scene': mainmenu.MainMenu
                    })
                ), 0x6a6a6a, centered=True
            )
        )

        