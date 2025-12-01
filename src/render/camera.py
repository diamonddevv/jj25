import pygame
import typing

from src import consts

type _SurfaceOp = typing.Callable[[pygame.Surface], typing.Any]
type _BlitParams = tuple[pygame.Surface, pygame.Vector2]
type _Op = _SurfaceOp | _BlitParams

class Camera():

    def __init__(self) -> None:
        self.focus = pygame.Vector2(0, 0)
        self.zoom = 1.0


        self._frame_blits: dict[int, tuple[list[_SurfaceOp], list[_BlitParams]]] = {}

    def w2s(self, world: pygame.Vector2) -> pygame.Vector2:
        pivot = (pygame.Vector2(consts.CANVAS_DIMS) / 2)
        return (world - self.focus) * self.zoom + pivot
    
    def w2s_up(self, x: float, y: float) -> pygame.Vector2:
        return self.w2s(pygame.Vector2(x, y))
    
    def scale_zoom(self, x: float) -> float:
        return x * self.zoom
    
    def with_zindex(self, op: _SurfaceOp, zindex: int = 0):
        layer = self._frame_blits.get(zindex, ([], []))
        layer[0].append(op)
        self._frame_blits[zindex] = layer

    def with_zindex_blit(self, params: _BlitParams, zindex: int = 0):
        layer = self._frame_blits.get(zindex, ([], []))
        layer[1].append(params)
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

            print(vp.w - clip.w, vp.h - clip.h)

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
        for zindex in sorted(self._frame_blits, key=lambda k: k):
            layer = self._frame_blits[zindex]
            canvas.blits(layer[1])
            for op in layer[0]:
                op(canvas)

        self._frame_blits = {}