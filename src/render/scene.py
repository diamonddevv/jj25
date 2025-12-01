from __future__ import annotations
from src.render import camera


class SceneManager():
    def __init__(self, default: type[Scene]) -> None:
        self.current = default()


    def draw_current(self, camera: camera.Camera):
        self.current.draw(camera)

    def update_current(self, dt: float, camera: camera.Camera):
        self.current.update(dt, camera)

    def change(self, scene: type[Scene]):
        self.current = scene()


class Scene():
    def __init__(self) -> None:
        pass

    def draw(self, camera: camera.Camera):
        pass

    def update(self, dt: float, camera: camera.Camera):
        pass