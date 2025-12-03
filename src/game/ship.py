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
                '2': ((2, 0), pygame.Rect(0, 0, 16, 4)), # top corner left
                '3': ((3, 0), pygame.Rect(0, 0, 16, 4)), # top corner right
                '4': ((0, 1), pygame.Rect(0, 11, 16, 5)), # bottom

                '5': ((2, 1), pygame.Rect(0, 0, 5, 16)), # side left
                '6': ((3, 1), pygame.Rect(11, 0, 5, 16)), # side right
                '7': ((2, 2), pygame.Rect(0, 11, 16, 16)), # bottom corner left
                '8': ((3, 2), pygame.Rect(0, 11, 16, 16)), # bottom corner right

                '9': ((5,2), None) # ship body
            },
            "2111111111111113" +
            "5000000000000006" + 
            "5000000000000006" +
            "5000000000000006" +
            "5000000000000006" +
            "7444444444444448" +
            "9999999999999999" +
            "9999999999999999" +
            "9999999999999999" +
            "9999999999999999"
            ,
            16
        )

        self.map_colliders = map.MapRenderer.compile_colliders(self.map_data, consts.DRAW_SCALE, pygame.Vector2())

    def draw(self, cam: camera.Camera):
        map.MapRenderer.draw_map(cam, pygame.Vector2(), self.map_data, consts.DRAW_SCALE)

    def update(self, dt: float, cam: camera.Camera):
        pass