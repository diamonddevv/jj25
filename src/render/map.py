import pygame

from src.render import spritesheet
from src.render import camera


class MapRenderer():
    type MapData = tuple[
        int, int, int,
        list[tuple[pygame.Surface, pygame.Rect | None] | None]
    ]

    @staticmethod
    def compile_map(spritesheet: spritesheet.Spritesheet, keys: dict[str, tuple[tuple[int, int] | None, pygame.Rect | None]], shape: str, width: int) -> MapData:
        tiles: list[tuple[pygame.Surface, pygame.Rect | None] | None] = []

        for char in shape:
            pos = keys[char][0]
            if pos is not None:
                tiles.append(
                    (spritesheet.get_cell(*pos), keys[char][1])
                )
            else:
                tiles.append(None)

        return (width, spritesheet.cell_w, spritesheet.cell_h, tiles)
    
    @staticmethod
    def compile_colliders(data: MapData, scale: float, pos: pygame.Vector2) -> list[pygame.Rect]:
        size, tw, th, tiles = data
        topleft = pos.copy()
        rects: list[pygame.Rect] = []

        idx = 0
        for pair in tiles:
            if pair is not None:
                _, collider = pair
                if collider is not None:
                    r = pygame.Rect(pos + pygame.Vector2(collider.topleft) * scale, pygame.Vector2(collider.size) * scale)
                    rects.append(r)

            pos.x += tw * scale
            idx += 1
            if idx >= size:
                idx = 0
                pos.x = topleft.x
                pos.y += th * scale

        return rects
        
    @staticmethod
    def draw_map(cam: camera.Camera, pos: pygame.Vector2, data: MapData, scale: float, zindex: int = -5):
        size, tw, th, tiles = data
        topleft = pos.copy()

        idx = 0
        for pair in tiles:
            if pair is not None:
                tile, _ = pair
                cam.blit(tile, pos, False, scale, zindex=zindex)
                
            pos.x += tw * scale
            idx += 1
            if idx >= size:
                idx = 0
                pos.x = topleft.x
                pos.y += th * scale
            