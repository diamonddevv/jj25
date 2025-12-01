import pygame

from src.render import scene
from src.render.camera import Camera

class TestScene(scene.Scene):
    def __init__(self) -> None:
        super().__init__()
        self.age = 0

    def draw(self, camera: Camera):
        super().draw(camera)

        camera.with_zindex(lambda s: s.fill(
            (127, 0, 127)
        ), zindex=-999)

    def update(self, dt: float, camera: Camera):
        super().update(dt, camera)