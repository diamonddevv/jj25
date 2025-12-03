import pygame

from src import util
from src import consts
from src.render import spritesheet
from src.render import animate
from src.render import camera


class Interactable():
    def __init__(self, pos: pygame.Vector2 = pygame.Vector2()) -> None:
        self.pos = pos

class Cannon(Interactable):
    ANIM_IDLE: str = "idle"
    ANIM_SELECTABLE: str = "selectable"
    ANIM_FIRE: str = "firing"

    def __init__(self, pos: pygame.Vector2 = pygame.Vector2()) -> None:
        super().__init__(pos)
        self.spritesheet = spritesheet.Spritesheet(util.load_texture('res/cannon.png'))
        self.collider_base = pygame.Rect(0, -8, 12, 5)
        self.collider = pygame.Rect(0, 0, 0, 0)
        self.anim_tex = animate.AnimatedTexture(self.spritesheet,
                                                {
                                                    Cannon.ANIM_IDLE: (4, [(0, 0)]),
                                                    Cannon.ANIM_SELECTABLE: (4, [(1, 0)]),
                                                    Cannon.ANIM_FIRE: (4, [(0, 1), (0, 2), (0, 3), (0, 4)])
                                                })

    def draw(self, cam: camera.Camera):
        cam.blit(
            self.anim_tex.get_frame(), self.pos, scale=consts.DRAW_SCALE,zindex=-2
        )

    def update(self, dt: float, cam: camera.Camera):
        self.anim_tex.tick(dt)
        self.collider = pygame.Rect(self.pos - pygame.Vector2(self.collider_base.size) * consts.DRAW_SCALE / 2 + pygame.Vector2(self.collider_base.topleft) * consts.DRAW_SCALE, pygame.Vector2(self.collider_base.size) * consts.DRAW_SCALE)
