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


class LoseScene(menu.MenuScene):

    def __init__(self, camera: camera.Camera, ctx: tuple) -> None:
        super().__init__(camera, ctx)
        camera.fill_col = 0x2890dc

        self.lose = pygame.mixer.Sound('res/sound/lose.ogg')
        self.lose.play()

        self.container.add(
            ui.UiText(pygame.Vector2(consts.CANVAS_DIMS[0] / 2, 125),
                      lambda: "loser", 3, 0x000000, centered=True, sfsans=True)
        )
        self.container.add(
            ui.UiText(pygame.Vector2(consts.CANVAS_DIMS[0] / 2, 530),
                      lambda: (
                          "Yer crew was overpowered by the foes.."
                      ) if not ctx[0] else (
                          "Arr! Ye perished of scurvy. (maybe eat more lemons next time..)"
                      ), 2, 0x000000, centered=True)
        )
        
        self.container.add(
            ui.UiButton(
                pygame.Vector2(consts.CANVAS_DIMS[0] / 2, consts.CANVAS_DIMS[1] - 128),
                lambda: "ok", 4, lambda: pygame.event.post(
                    pygame.Event(event.CHANGE_SCENE, {
                        'scene': mainmenu.MainMenu,
                        'ctx': ()
                    })
                ), 0x000000, centered=True
            )
        )

        