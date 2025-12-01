import pygame
import math
import typing

from src import shared
from src.render import camera

class Pirate():

    SPRITE_PIRATE: tuple[int, int] = (0, 0)

    def __init__(self) -> None:
        self.position = pygame.Vector2()
        self.speed = 100.0
        self.rotation = 0.0
        self.health = 100.0

    def draw(self, cam: camera.Camera):
        cam.blit(
            shared.SPRITESHEET.get_cell(*Pirate.SPRITE_PIRATE),
            self.position, True, scale=4, rotation=self.rotation
        )

    def update(self, dt: float, cam: camera.Camera):
        self.position += self.get_movement(dt).elementwise() * dt * self.speed

    def get_movement(self, dt: float) -> pygame.Vector2:
        return pygame.Vector2()
    
class PlayerPirate(Pirate):
    def get_movement(self, dt: float) -> pygame.Vector2:
        keys = pygame.key.get_pressed()
        vec = pygame.Vector2()

        if keys[pygame.K_w]: vec.y -= 1
        if keys[pygame.K_a]: vec.x -= 1
        if keys[pygame.K_s]: vec.y += 1
        if keys[pygame.K_d]: vec.x += 1

        return vec