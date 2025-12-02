import pygame

from src.render import spritesheet
from src.render import camera


class MapRenderer():
    type MapData = tuple[
        int, int, int,
        list[pygame.Surface]
    ]

    @staticmethod
    def compile_map(spritesheet: spritesheet.Spritesheet, keys: dict[str, tuple[int, int]], shape: str, width: int) -> MapData:
        tiles: list[pygame.Surface] = []

        for char in shape:
            tiles.append(spritesheet.get_cell(*keys[char]))

        return (width, spritesheet.cell_w, spritesheet.cell_h, tiles)
        
    @staticmethod
    def draw_map(cam: camera.Camera, pos: pygame.Vector2, data: MapData, scale: float, zindex: int = -5):
        size, tw, th, tiles = data
        topleft = pos.copy()

        idx = 0
        for tile in tiles:
            cam.blit(tile, pos, False, scale, zindex=zindex)
            pos.x += tw * scale
            idx += 1
            if idx >= size:
                idx = 0
                pos.x = topleft.x
                pos.y += th * scale
            