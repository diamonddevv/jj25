from __future__ import annotations
import pygame
import typing
import random

from src import consts

type _SurfaceOp = typing.Callable[[pygame.Surface], typing.Any]
type _BlitParams = tuple[pygame.Surface, pygame.Vector2]
type _Op = _SurfaceOp | _BlitParams

class Camera():

    def __init__(self, window: pygame.Window) -> None:
        self.focus = pygame.Vector2(0, 0)
        self.zoom = 1.0
        self.fill_col = 0x0

        self.window = window

        self._frame_blits: dict[int, tuple[list[_SurfaceOp], list[_BlitParams]]] = {}

    def w2s(self, world: pygame.Vector2) -> pygame.Vector2:
        pivot = (pygame.Vector2(consts.CANVAS_DIMS) / 2)
        return (world - self.focus) * self.zoom + pivot
    
    def w2s_up(self, x: float, y: float) -> pygame.Vector2:
        return self.w2s(pygame.Vector2(x, y))
    
    def w2s_r(self, rect: pygame.Rect) -> pygame.Rect:
        return pygame.Rect(self.w2s_up(*rect.topleft), pygame.Vector2(rect.size) * self.zoom)
    
    def scale_zoom(self, x: float) -> float:
        return x * self.zoom
    
    def with_zindex(self, op: _SurfaceOp, zindex: int = 0):
        layer = self._frame_blits.get(zindex, ([], []))
        layer[0].append(op)
        self._frame_blits[zindex] = layer

    def with_zindex_provider[T](self, op: typing.Callable[[pygame.Surface, T], typing.Any], t: T, zindex: int = 0):
        layer = self._frame_blits.get(zindex, ([], []))
        layer[0].append(lambda s: op(s, t))
        self._frame_blits[zindex] = layer

    def with_zindex_blit(self, params: _BlitParams, centered: bool = False, zindex: int = 0):
        layer = self._frame_blits.get(zindex, ([], []))
        layer[1].append((params[0], (pygame.Vector2(params[1]) - pygame.Vector2(params[0].size) / 2) if centered else params[1]))
        self._frame_blits[zindex] = layer

    def vp(self, screencoord: bool = False) -> pygame.Rect:
        dims = pygame.Vector2(consts.CANVAS_DIMS) / self.zoom
        rect = pygame.Rect((self.focus - dims / 2), dims)
        if screencoord:
            rect.topleft = self.w2s_up(*rect.topleft)
            rect.size = consts.CANVAS_DIMS
        return rect
    
    def clamp_vp(self, area: pygame.Rect):
        vp = self.vp(screencoord=True)

        if area.contains(vp):
            return
        else:
            clip = area.clip(vp)

            left = abs(vp.x - clip.x)
            up = abs(vp.y - clip.y)
            right = abs(vp.w - clip.w) if clip.x > area.x else 0
            down = abs(vp.h - clip.h) if clip.y > area.y else 0

            self.focus.x += left
            self.focus.x -= right
            self.focus.y += up
            self.focus.y -= down

    def absolute(self) -> Camera:
        return AbsoluteCamera(self)

    def get_mouse_pos(self) -> pygame.Vector2:
        return (pygame.Vector2(pygame.mouse.get_pos()).elementwise() / pygame.Vector2(self.window.size)).elementwise() * pygame.Vector2(consts.CANVAS_DIMS)

    def blit(self, surface: pygame.Surface, pos: pygame.Vector2, centered: bool = True, scale: float = 1, rotation: float = 0.0, skip_cull: bool = False, zindex: int = 0):

        # resolve transformations
        surface = pygame.transform.scale_by(surface, self.zoom * scale)
        if rotation != 0.0:
            surface = pygame.transform.rotate(surface, -rotation)

        # resolve position
        screen_pos = self.w2s(pos)
        if centered:
            screen_pos = pygame.Vector2(surface.get_rect(center=screen_pos).topleft)

        # add op
        self.with_zindex_blit((surface, screen_pos), zindex=zindex)


    def render(self, canvas: pygame.Surface):
        canvas.fill(self.fill_col)
        for zindex in sorted(self._frame_blits, key=lambda k: k):
            layer = self._frame_blits[zindex]
            canvas.blits(layer[1])
            for op in layer[0]:
                op(canvas)

        self._frame_blits = {}

class AbsoluteCamera(Camera):
    def __init__(self, camera: Camera) -> None:
        super().__init__(camera.window)
        self.parent = camera

    def w2s(self, world: pygame.Vector2) -> pygame.Vector2:
        return world
    
    def scale_zoom(self, x: float) -> float:
        return x

    def with_zindex(self, op: _SurfaceOp, zindex: int = 0):
        layer = self.parent._frame_blits.get(zindex, ([], []))
        layer[0].append(op)
        self.parent._frame_blits[zindex] = layer

    def with_zindex_provider[T](self, op: typing.Callable[[pygame.Surface, T], typing.Any], t: T, zindex: int = 0):
        layer = self.parent._frame_blits.get(zindex, ([], []))
        layer[0].append(lambda s: op(s, t))
        self.parent._frame_blits[zindex] = layer

    def with_zindex_blit(self, params: _BlitParams, centered: bool = False, zindex: int = 0):
        layer = self.parent._frame_blits.get(zindex, ([], []))
        layer[1].append((params[0], (pygame.Vector2(params[1]) - pygame.Vector2(params[0].size) / 2) if centered else params[1]))
        self.parent._frame_blits[zindex] = layer