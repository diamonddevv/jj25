import pygame

from src import util
from src import event
from src import consts
from src.render import spritesheet
from src.render import animate
from src.render import camera
from src.game import fireable


class Interactable():
    def __init__(self, pos: pygame.Vector2 = pygame.Vector2()) -> None:
        self.position = pos
        self.collider = pygame.Rect(0, 0, 0, 0)
        self.highlight = False

    def draw(self, cam: camera.Camera):
        pass

    def update(self, dt: float, cam: camera.Camera):
        pass

class Cannon(Interactable):
    ANIM_IDLE: str = "idle"
    ANIM_SELECTABLE: str = "selectable"
    ANIM_FIRE: str = "firing"

    COOLDOWN: float = 1.5

    def __init__(self, pos: pygame.Vector2 = pygame.Vector2()) -> None:
        super().__init__(pos)
        self.spritesheet = spritesheet.Spritesheet(util.load_texture('res/interactable.png'))
        self.collider_base = pygame.Rect(0, -8, 12, 5)
        self.anim_tex = animate.AnimatedTexture(self.spritesheet,
                                                {
                                                    Cannon.ANIM_IDLE: (4, [(0, 0)]),
                                                    Cannon.ANIM_SELECTABLE: (4, [(1, 0)]),
                                                    Cannon.ANIM_FIRE: (6, [(0, 1), (1, 1), (2, 1), (3, 1)])
                                                })
        
        self.cooldown = 0.0

    def draw(self, cam: camera.Camera):
        cam.blit(
            self.anim_tex.get_frame(), self.position, scale=consts.DRAW_SCALE,zindex=-2
        )

    def update(self, dt: float, cam: camera.Camera):

        if self.cooldown <= 0:
            self.anim_tex.set_anim(Cannon.ANIM_SELECTABLE if self.highlight else Cannon.ANIM_IDLE)

        if self.cooldown > 0:
            self.cooldown -= dt
        self.anim_tex.tick(dt)
        self.collider = pygame.Rect(self.position - pygame.Vector2(self.collider_base.size) * consts.DRAW_SCALE / 2 + pygame.Vector2(self.collider_base.topleft) * consts.DRAW_SCALE, pygame.Vector2(self.collider_base.size) * consts.DRAW_SCALE)

    def fire(self, fireable: fireable.Fireable):
        if self.cooldown <= 0:
            self.anim_tex.set_anim(Cannon.ANIM_FIRE, oneshot=True)
            self.anim_tex.last_anim = Cannon.ANIM_IDLE
            self.cooldown = Cannon.COOLDOWN
            event.sequence([
                (fireable.hide, 0.0),
                (fireable.show, 4/6),
                (lambda: fireable._start_fire_anim(self.position), 0.0)
            ])