import pygame

from src import util
from src import consts
from src.render import camera
from src.render import spritesheet

class Item():
    type _ItemEntry = tuple[
        tuple[int, int], # tilesheet pos
        str # name
    ]

    ITEMS: dict[int, _ItemEntry] = {
        0: ((0, 0), "Cannonball"),
        1: ((1, 0), "Bottle o' Rum"),
        2: ((2, 0), "Parrot"),
    }

    FIRE_SPEED: float = 400
    FIRE_ROT_SPEED: float = 360

    def __init__(self, id: int, pos: pygame.Vector2 = pygame.Vector2()) -> None:
        self.pos = pos
        self.id = id
        self.texture = spritesheet.Spritesheet(util.load_texture('res/items.png'))
        self.flip_texture = False
        self.held = False
        self.interactable = False
        self.hidden = False
        self.fired = False
        self.rotation = 0.0
        self.fired_up = True

    def draw(self, cam: camera.Camera):
        if not self.hidden:
            cam.blit(pygame.transform.flip(self.texture.get_cell(*Item.ITEMS[self.id][0]), self.flip_texture, False), self.pos, rotation=self.rotation, scale=consts.DRAW_SCALE, zindex=1 if self.held else -1)

    def update(self, dt: float, cam: camera.Camera):
        if self.fired:
            self.pos.y -= Item.FIRE_SPEED * dt * (1 if self.fired_up else -1)
            self.rotation += Item.FIRE_ROT_SPEED * dt

    def can_be_picked_up(self) -> bool:
        return not self.held and self.interactable and not self.hidden
    
    def name(self) -> str:
        return Item.ITEMS[self.id][1]
    
    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def _start_fire_anim(self, position: pygame.Vector2):
        self.pos = position.copy()
        self.fired = True
        self.interactable = False

    