import pygame

from src.render import scene
from src.render.camera import Camera

class GameScene(scene.Scene):
    def __init__(self) -> None:
        super().__init__()
        self.age = 0.0

    def draw(self, camera: Camera):
        super().draw(camera)

    def update(self, dt: float, camera: Camera):
        super().update(dt, camera)