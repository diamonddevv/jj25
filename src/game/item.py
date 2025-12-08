import pygame
import random

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
        str, # name
        float, # dmg mult
        bool, # spawns damage marks
        bool, # fixes damage marks
        bool, # gets you drunk
        bool, # cures scurvy
        bool, # ais launch
        bool, # ais pick up
        bool # in barrels
    ]

    ITEMS: list[_ItemEntry] = [
        ((0, 0), "Cannonball", 3.0, True, False, False, False, True, True, True),
        ((1, 0), "Bottle o' Rum", 0.8, True, False, True, False, True, True, True),
        ((2, 0), "Parrot", 0.2, True, False, False, False, True, True, True),
        ((3, 0), "Wood", 0, False, True, False, False, False, True, True),
        ((4, 0), "Lemon", 0.8, False, False, False, True, True, True, True),
        ((5, 0), "Perished Matey", 2.5, True, False, False, False, False, False, True),
        ((6, 0), "Jar of Dirt", 5, True, False, False, False, True, True, True),
    ]

    

    def __init__(self, id: int, pos: pygame.Vector2 = pygame.Vector2()) -> None:
        super().__init__()
        self.position = pos
        self.id = id
        self.texture = spritesheet.Spritesheet(util.load_texture('res/items.png'))
        self.flip_texture = False
        self.held = False
        self.removal_mark = False
        self.rotation = 0.0
        self.random_variance: float = random.random()

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
    
    def damage_mult(self) -> float:
        return Item.ITEMS[self.id][2]
    
    def causes_damage(self) -> bool:
        return Item.ITEMS[self.id][3]
    
    def fixes_damage(self) -> bool:
        return Item.ITEMS[self.id][4]
    
    def gets_you_drunk(self) -> bool:
        return Item.ITEMS[self.id][5]
    
    def cures_scurvy(self) -> bool:
        return Item.ITEMS[self.id][6]
    
    def ai_launches(self) -> bool:
        return Item.ITEMS[self.id][7]
    
    def ai_picks_up(self) -> bool:
        return Item.ITEMS[self.id][8]
    
    def in_barrels(self) -> bool:
        return Item.ITEMS[self.id][9]
    
    def set_position(self, position: pygame.Vector2):
        self.position = position

    def fire(self, firer: pirate.Pirate, cannon: interact.Cannon):
        super().fire(firer, cannon)
    
    

    