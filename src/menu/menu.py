import pygame

from src.render import camera
from src.render import scene
from src.render import ui


class MenuScene(scene.Scene):
    def __init__(self, camera: camera.Camera) -> None:
        super().__init__(camera)

        self.container = ui.UiContainer()

    def draw(self, camera: camera.Camera):
        super().draw(camera)
        self.container.draw(camera)
    
    def update(self, dt: float, camera: camera.Camera):
        super().update(dt, camera)
        self.container.update(dt, camera)