import pygame
import math

from src import shared
from src.render import camera

class Ship():

    def __init__(self) -> None:
        self.position = pygame.Vector2()
        self.health = 1000.0

    def draw(self, cam: camera.Camera):
        pass

    def update(self, dt: float, cam: camera.Camera):
        pass