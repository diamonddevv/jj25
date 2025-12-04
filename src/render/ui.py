from __future__ import annotations
import pygame
import typing

from src import consts
from src import util
from src.render import camera
from src.render import text
from src.game import pirate

class UiContainer():
    def __init__(self) -> None:
        self.elements: list[UiElement] = []

    def draw(self, cam: camera.Camera):
        for element in self.elements:
            if element.visible:
                element.draw(cam)

                if consts.DRAW_COLLISION_BOXES:
                    cam.with_zindex_provider(lambda s, r: pygame.draw.rect(s, 'green', r, 8), element.rect())

        if consts.DRAW_COLLISION_BOXES:
            cam.with_zindex_provider(lambda s, p: pygame.draw.circle(s, 'red', p, 8), cam.get_mouse_pos())

    def update(self, dt: float, cam: camera.Camera):
        mousepos = cam.get_mouse_pos()
        mousedown = pygame.mouse.get_just_pressed()[0]
        for element in self.elements:
            if element.visible:
                element.update(dt, cam)
                element.mouse_hover = element.rect().collidepoint(mousepos)
                if element.mouse_hover and mousedown:
                    element.on_click()

                

    def add(self, element: UiElement):
        self.elements.append(element)

class UiElement():
    def __init__(self, position: pygame.Vector2) -> None:
        self.position = position
        self.visible = True
        self.mouse_hover = False

    def draw(self, cam: camera.Camera):
        pass

    def update(self, dt: float, cam: camera.Camera):
        pass

    def on_click(self):
        pass

    def rect(self) -> pygame.Rect:
        return pygame.Rect(0, 0, 0, 0)
    

class UiText(UiElement):
    def __init__(self, position: pygame.Vector2, text_provider: typing.Callable[[], str], scale: float, color: pygame.typing.ColorLike | None = None, sfsans: bool = False, centered: bool = False) -> None:
        super().__init__(position)
        self.text_provider = text_provider
        self.scale = scale
        self.color = color
        self.sfsans = sfsans
        self.centered = centered

    def draw(self, cam: camera.Camera):
        font = text.sfsans() if self.sfsans else text.glyphxel()
        cam.with_zindex_blit(
                (
                    font.render_adv(self.text_provider(), self.scale, None if self.color is None else (~int(pygame.Color(self.color)) if self.mouse_hover else self.color)),
                    self.position
                ), centered=self.centered
            )
        
class UiButton(UiText):
    def __init__(self, position: pygame.Vector2, text_provider: typing.Callable[[], str], scale: float, onclick: typing.Callable, color: pygame.typing.ColorLike | None = None, sfsans: bool = False, centered: bool = False) -> None:
        super().__init__(position, text_provider, scale, color, sfsans, centered)
        self.on_click = onclick

    def rect(self) -> pygame.Rect:
        font = text.sfsans() if self.sfsans else text.glyphxel()
        surface = font.render_adv(self.text_provider(), self.scale, self.color)
        if self.centered:
            return surface.get_rect(center=self.position)
        else:
            return surface.get_rect(topleft=self.position)
        
class UiPirate(UiElement):
    def __init__(self, position: pygame.Vector2, p: pirate.Pirate) -> None:
        super().__init__(position)
        self.pirate = p
        self.pirate.position = self.position

        self.reverse = False

        self.pirate.update_anim = False
        self.pirate.anim_tex.set_anim(pirate.Pirate.ANIM_RUN)

    def draw(self, cam: camera.Camera):
        super().draw(cam)
        self.pirate.draw(cam.absolute())

    def update(self, dt: float, cam: camera.Camera):
        super().update(dt, cam)
        self.pirate.update(dt, cam.absolute())

        self.pirate.position.x += self.pirate.speed * dt / 2 * (-1 if self.reverse else 1)
        self.pirate.anim_tex.flipped = self.reverse
        if self.pirate.position.x >= consts.CANVAS_DIMS[0] - 128:
            self.reverse = True
        if self.pirate.position.x <=  128:
            self.reverse = False

class UiTexture(UiElement):
    def __init__(self, position: pygame.Vector2, path: str, scale: float = 1, centered: bool = True) -> None:
        super().__init__(position)
        self.sprite = util.load_texture(path)
        self.scale = scale
        self.centered = centered

    def draw(self, cam: camera.Camera):
        cam.absolute().blit(self.sprite, self.position, scale=self.scale, centered=self.centered)