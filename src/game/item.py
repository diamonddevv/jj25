import pygame

from src import util
from src.render import camera
from src.render import spritesheet

class Item():
    ITEM_INDICES: dict[int, tuple[int, int]] = {
        0: (0, 0)
    }

    def __init__(self, id: int) -> None:
        self.pos = pygame.Vector2()
        self.id = id
        self.texture = spritesheet.Spritesheet(util.load_texture('res/items.png'))
        self.held = False

    def draw(self, cam: camera.Camera):
        cam.blit(self.texture.get_cell(*Item.ITEM_INDICES[self.id]), self.pos, scale=4)

    def update(self, dt: float, cam: camera.Camera):
        pass

    def can_be_picked_up(self) -> bool:
        return not self.held

    