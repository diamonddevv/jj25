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
from src.menu import credits


class MainMenu(menu.MenuScene):
    def __init__(self, camera: camera.Camera) -> None:
        super().__init__(camera)
        camera.fill_col = 0x2890dc

        self.container.add(
            ui.UiText(pygame.Vector2(consts.CANVAS_DIMS[0] / 2, 200),
                      lambda: consts.TITLE.upper(), 4, 0x000000, centered=True, sfsans=True)
        )
        self.container.add(
            ui.UiText(pygame.Vector2(consts.CANVAS_DIMS[0] / 2, 250),
                      lambda: consts.SUBTITLE, 2, 0x000000, centered=True)
        )
        self.container.add(
            ui.UiPirate(pygame.Vector2(128, consts.CANVAS_DIMS[1] - 64), pirate.Pirate(None, pygame.Vector2())) # type: ignore
        )
        self.container.add(
            ui.UiButton(
                pygame.Vector2(consts.CANVAS_DIMS[0] / 2, 500),
                lambda: "Play", 4, lambda: pygame.event.post(
                    pygame.Event(event.CHANGE_SCENE, {
                        'scene': game.GameScene
                    })
                ), 0x000000, centered=True
            )
        )
        self.container.add(
            ui.UiButton(
                pygame.Vector2(consts.CANVAS_DIMS[0] / 2, 600),
                lambda: "Credits", 4, lambda: pygame.event.post(
                    pygame.Event(event.CHANGE_SCENE, {
                        'scene': credits.CreditsScene
                    })
                ), 0x000000, centered=True
            )
        )
        self.container.add(
            ui.UiButton(
                pygame.Vector2(consts.CANVAS_DIMS[0] / 2, 700),
                lambda: "Quit", 4, lambda: pygame.event.post(
                    pygame.Event(pygame.QUIT)
                ), 0x000000, centered=True
            )
        )

        self.container.add(
            ui.UiTexture(pygame.Vector2(20, 25), 'res/ddv.png', centered=False, scale=0.1)
        )
        self.container.add(
            ui.UiTexture(pygame.Vector2(80, 20), 'res/diamonddev.png', centered=False, scale=4)
        )

        