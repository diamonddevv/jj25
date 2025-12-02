import pygame
import math
import typing

from src import util
from src.render import spritesheet
from src.render import camera
from src.render import animate

class Pirate():

    def __init__(self) -> None:
        self.position = pygame.Vector2()
        self.speed = 300.0
        self.health = 100.0

        self.anim_tex = animate.AnimatedTexture(spritesheet.Spritesheet(util.load_texture('res/pirate.png')), {
            'idle': (4, [(0, 0), (1, 0)]),
            'run': (4, [(0, 1), (1, 1)]),
            'crouch': (4, [(2, 0)])
        })

    def draw(self, cam: camera.Camera):
        cam.blit(
            self.anim_tex.get_frame(),
            self.position, True, scale=8
        )

    def update(self, dt: float, cam: camera.Camera):
        movement = self.get_movement(dt)

        self.anim_tex.set_anim('idle' if movement == pygame.Vector2() else 'run')
        
        if movement.x != 0:
            self.anim_tex.flipped = movement.x < 0

        self.anim_tex.tick(dt)
        self.position += movement.elementwise() * dt * self.speed

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

        if vec.length() != 0:
            vec.normalize_ip()

        return vec