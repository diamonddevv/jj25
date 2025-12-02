import pygame
import math

from src import util
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
                '0': (0, 0), # plank
                '1': (1, 0), # top
                '2': (2, 0), # top corner left
                '3': (3, 0), # top corner right
                '4': (0, 1), # bottom

                '5': (2, 1), # side left
                '6': (3, 1), # side right
                '7': (2, 2), # bottom corner left
                '8': (3, 2), # bottom corner right
            },
            "2111111111111113" +
            "5000000000000006" + 
            "5000000000000006" +
            "5000000000000006" +
            "5000000000000006" +
            "7444444444444448",
            16
        )

    def draw(self, cam: camera.Camera):
        map.MapRenderer.draw_map(cam, pygame.Vector2(), self.map_data, 8)

    def update(self, dt: float, cam: camera.Camera):
        pass