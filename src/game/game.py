import pygame
import typing

from src import consts
from src import event
from src.render import scene
from src.render import camera
from src.render import text
from src.game import item
from src.game import ship
from src.game import pirate
from src.game import interact
from src.game import manager

class GameScene(scene.Scene):

    def __init__(self, camera: camera.Camera, ctx: tuple) -> None:
        super().__init__(camera, ctx)
        
        camera.fill_col = 0x2890dc

        self.manager = manager.GameManager(camera)


    def draw(self, camera: camera.Camera):
        super().draw(camera)

        self.manager.draw(camera)
        

    def update(self, dt: float, camera: camera.Camera):
        super().update(dt, camera)

        camera.focus = pygame.Vector2(16 * consts.DRAW_SCALE * 16, 0)
        self.manager.update(dt, camera)
