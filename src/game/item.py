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

    def __init__(self, id: int, pos: pygame.Vector2 = pygame.Vector2()) -> None:
        self.pos = pos
        self.id = id
        self.texture = spritesheet.Spritesheet(util.load_texture('res/items.png'))
        self.held = False

    def draw(self, cam: camera.Camera):
        cam.blit(self.texture.get_cell(*Item.ITEMS[self.id][0]), self.pos, scale=consts.DRAW_SCALE, zindex=1 if self.held else -1)

    def update(self, dt: float, cam: camera.Camera):
        pass

    def can_be_picked_up(self) -> bool:
        return not self.held
    
    def name(self) -> str:
        return Item.ITEMS[self.id][1]

    