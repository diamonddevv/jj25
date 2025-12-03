import pygame
import math
import typing

from src import util
from src import consts
from src import event
from src.render import spritesheet
from src.render import camera
from src.render import animate
from src.render import text

from src.game import item
from src.game import interact

class Pirate():
    ANIM_IDLE: str = 'idle'
    ANIM_RUN: str = 'run'
    ANIM_CROUCH: str = 'crouch'
    ANIM_HOLD: str = 'hold'

    def __init__(self, interactables: list[interact.Interactable]) -> None:
        self.position = pygame.Vector2(100, 100)
        self.speed = 300.0
        self.reach = 80
        self.health = 100.0
        self.crouched = False
        self.held_item: item.Item | None = None
        self.collision_box = pygame.Rect(0, 0, 0, 0)

        self.interactables: list[interact.Interactable] = interactables
        self.collidables: list[typing.Callable[[], pygame.Rect]] = []

        self.anim_tex = animate.AnimatedTexture(spritesheet.Spritesheet(util.load_texture('res/pirate.png')), {
            Pirate.ANIM_IDLE: (4, [(0, 0), (1, 0)]),
            Pirate.ANIM_RUN: (4, [(0, 1), (1, 1)]),
            Pirate.ANIM_CROUCH + "-" + Pirate.ANIM_IDLE: (4, [(2, 0)]),
            Pirate.ANIM_CROUCH + "-" + Pirate.ANIM_RUN: (4, [(2, 1), (3, 1)]),

            Pirate.ANIM_IDLE + "-" + Pirate.ANIM_HOLD: (4, [(0, 3)]),
            Pirate.ANIM_RUN + "-" + Pirate.ANIM_HOLD: (4, [(0, 3), (1, 3)]),
            Pirate.ANIM_CROUCH + "-" + Pirate.ANIM_IDLE + "-" + Pirate.ANIM_HOLD: (4, [(0, 3)]),
            Pirate.ANIM_CROUCH + "-" + Pirate.ANIM_RUN + "-" + Pirate.ANIM_HOLD: (4, [(0, 3), (1, 3)])
        })

    def draw(self, cam: camera.Camera):
        cam.blit(
            self.anim_tex.get_frame(),
            self.position, True, scale=consts.DRAW_SCALE
        )

        if consts.DRAW_COLLISION_BOXES:
            cam.with_zindex(lambda s: pygame.draw.rect(s, 'red', cam.w2s_r(self.collision_box), 8), 10)

        if self.held_item is not None:
            self.held_item.flip_texture = self.anim_tex.flipped
            self.held_item.pos = self.position + pygame.Vector2(8 * (-1 if self.anim_tex.flipped else 1), -8 * consts.DRAW_SCALE)

    def update(self, dt: float, cam: camera.Camera):
        movement = self.get_movement(dt)

        anim = Pirate.ANIM_IDLE
        if movement != pygame.Vector2():
            anim = Pirate.ANIM_RUN

        if self.crouched:
            anim = Pirate.ANIM_CROUCH + "-" + anim

        if self.held_item is not None:
            anim = anim + "-" + Pirate.ANIM_HOLD

        self.anim_tex.set_anim(anim)
        
        if movement.x != 0:
            self.anim_tex.flipped = movement.x < 0

        self.anim_tex.tick(dt)
        self.collision_box = self.anim_tex.get_frame().get_rect(center=self.position).scale_by(consts.DRAW_SCALE)

        self.position += movement.elementwise() * dt * self.speed * (0.6 if self.crouched or self.held_item is not None else 1)

        for provider in self.collidables:
            collidable = provider()
            if pygame.Vector2(collidable.center).distance_squared_to(self.position) < 20000:
                resolution = util.resolve_collision(collidable, self.collision_box)
                self.position += resolution
                

    def get_movement(self, dt: float) -> pygame.Vector2:
        return pygame.Vector2()
    
    def track_collidable(self, rect: pygame.Rect):
        self.collidables.append(lambda: rect)

    def track_collidable_thing[T](self, t: T, func: typing.Callable[[T], pygame.Rect]):
        self.collidables.append(lambda: func(t))

    def closest_interactable(self) -> interact.Interactable:
        return sorted(self.interactables, key=lambda i: self.position.distance_squared_to(i.pos))[0]

    @staticmethod
    def _clamp(x, lo, hi):
        return max(min(x, hi), lo)
    
class PlayerPirate(Pirate):

    KEY_UP: int = pygame.K_w
    KEY_DOWN: int = pygame.K_s
    KEY_LEFT: int = pygame.K_a
    KEY_RIGHT: int = pygame.K_d
    KEY_CROUCH: int = pygame.K_LSHIFT
    KEY_INTERACT: int = pygame.K_SPACE

    def get_movement(self, dt: float) -> pygame.Vector2:
        keys = pygame.key.get_pressed()
        vec = pygame.Vector2()

        if keys[PlayerPirate.KEY_UP]: vec.y -= 1
        if keys[PlayerPirate.KEY_LEFT]: vec.x -= 1
        if keys[PlayerPirate.KEY_DOWN]: vec.y += 1
        if keys[PlayerPirate.KEY_RIGHT]: vec.x += 1

        self.crouched = keys[PlayerPirate.KEY_CROUCH]

        if vec.length() != 0:
            vec.normalize_ip()

        return vec
    
    def draw(self, cam: camera.Camera):
        super().draw(cam)

        # hud
        if self.held_item is not None:
            cam.with_zindex_blit(
                (
                    text.glyphxel().render_adv(f"Held Item: {self.held_item.name()}", 2),
                    pygame.Vector2(20, 20)
                ), consts.HUD_LAYER
            )

        # colliders
        if consts.DRAW_COLLISION_BOXES:
            for provider in self.collidables:
                cam.with_zindex_provider(lambda s, r: pygame.draw.rect(s, 'green', cam.w2s_r(r), 8), provider(), 10)
    
    def update(self, dt: float, cam: camera.Camera):
        super().update(dt, cam)

        for i in self.interactables:
            i.highlight = False
        if self.held_item is not None:
            closest = self.closest_interactable()
            closest.highlight = self.position.distance_squared_to(closest.pos) <= self.reach ** 2

        pressed = pygame.key.get_just_pressed()
        if pressed[PlayerPirate.KEY_INTERACT]:
            if self.held_item is None:
                pygame.event.post(pygame.event.Event(event.PIRATE_INTERACT, {
                    'pirate': self
                }))
            else:
                closest = self.closest_interactable()
                if closest.highlight and isinstance(closest, interact.Cannon):
                    pygame.event.post(pygame.event.Event(event.FIRE_ITEM, {
                        'pirate': self,
                        'item': self.held_item,
                        'cannon': closest,
                    }))
                    self.held_item = None
                else:
                    self.held_item.pos = self.position.copy() + pygame.Vector2(0, 16)
                    self.held_item.held = False
                    self.held_item = None