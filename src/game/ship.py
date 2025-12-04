import pygame
import math

from src import util
from src import consts
from src.render import map
from src.render import spritesheet
from src.render import camera

class Ship():

    def __init__(self) -> None:
        self.position = pygame.Vector2()
        self.health = 1000.0

        self.map_data = map.MapRenderer.compile_map(
            spritesheet.Spritesheet(util.load_texture('res/ship.png')),
            {
                ' ': (None, None), # nothing
                '0': ((0, 0), None), # plank
                '1': ((1, 0), pygame.Rect(0, 0, 16, 4)), # top
                '2': (None, pygame.Rect(0, 0, 16, 4)), # top corner left
                '3': (None, pygame.Rect(0, 0, 16, 4)), # top corner right
                '4': ((0, 1), pygame.Rect(0, 11, 16, 5)), # bottom

                '5': (None, pygame.Rect(0, 0, 5, 16)), # side left
                '6': (None, pygame.Rect(11, 0, 5, 16)), # side right
                '7': (None, pygame.Rect(0, 11, 16, 16)), # bottom corner left
                '8': (None, pygame.Rect(0, 11, 16, 16)), # bottom corner right

                '9': ((5,2), None) # ship body
            },
            "21111111111111111111111111111113" +
            "50000000000000000000000000000006" + 
            "50000000000000000000000000000006" + 
            "50000000000000000000000000000006" +
            "50000000000000000000000000000006" +
            "50000000000000000000000000000006" +
            "74444444444444444444444444444448" +
            "99999999999999999999999999999999" +
            "99999999999999999999999999999999"
            ,
            32
        )

        self.map_colliders = map.MapRenderer.compile_colliders(self.map_data, consts.DRAW_SCALE, pygame.Vector2())

    def draw(self, cam: camera.Camera):
        map.MapRenderer.draw_map(cam, pygame.Vector2(), self.map_data, consts.DRAW_SCALE)

    def get_tile_center(self, cam: camera.Camera, x: int, y: int) -> pygame.Vector2:
        return map.MapRenderer.get_tile_center(
            x, y, cam, pygame.Vector2(), self.map_data, consts.DRAW_SCALE
        )

    def update(self, dt: float, cam: camera.Camera):
        pass