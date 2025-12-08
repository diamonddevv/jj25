from __future__ import annotations
from src.render import camera


class SceneManager():
    def __init__(self, camera: camera.Camera, default: type[Scene], ctx: tuple) -> None:
        self.current = default(camera, ctx)


    def draw_current(self, camera: camera.Camera):
        self.current.draw(camera)

    def update_current(self, dt: float, camera: camera.Camera):
        self.current.update(dt, camera)

    def change(self, camera: camera.Camera, scene: type[Scene], ctx: tuple):
        self.current = scene(camera, ctx)


class Scene():
    def __init__(self, camera: camera.Camera, ctx: tuple) -> None:
        pass

    def draw(self, camera: camera.Camera):
        pass

    def update(self, dt: float, camera: camera.Camera):
        pass