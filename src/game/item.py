import pygame

from src import util
from src import event
from src import consts
from src.render import camera
from src.render import spritesheet
from src.game import fireable
from src.game import pirate
from src.game import interact

class Item(fireable.Fireable):
    type _ItemEntry = tuple[
        tuple[int, int], # tilesheet pos
        str # name
    ]

    ITEMS: dict[int, _ItemEntry] = {
        0: ((0, 0), "Cannonball"),
        1: ((1, 0), "Bottle o' Rum"),
        2: ((2, 0), "Parrot"),
        3: ((3, 0), "Wood"),
    }

    

    def __init__(self, id: int, pos: pygame.Vector2 = pygame.Vector2()) -> None:
        super().__init__()
        self.position = pos
        self.id = id
        self.texture = spritesheet.Spritesheet(util.load_texture('res/items.png'))
        self.flip_texture = False
        self.held = False
        self.removal_mark = False
        self.rotation = 0.0

    def draw(self, cam: camera.Camera):
        if not self.hidden:
            cam.blit(pygame.transform.flip(self.texture.get_cell(*Item.ITEMS[self.id][0]), self.flip_texture, False), self.position, rotation=self.rotation, scale=consts.DRAW_SCALE, zindex=1 if self.held else -1)

    def update(self, dt: float, cam: camera.Camera):
        if self.fired:
            self.position.y -= fireable.Fireable.FIRE_SPEED * dt * (1 if self.fired_up else -1)
            self.rotation += fireable.Fireable.FIRE_ROT_SPEED * dt

    def can_be_picked_up(self) -> bool:
        return not self.held and not self.fired and not self.hidden and not self.removal_mark
    
    def name(self) -> str:
        return Item.ITEMS[self.id][1]
    
    def set_position(self, position: pygame.Vector2):
        self.position = position

    def fire(self, firer: pirate.Pirate, cannon: interact.Cannon):
        super().fire(firer, cannon)
    
    

    