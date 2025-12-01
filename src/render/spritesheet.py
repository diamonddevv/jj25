import pygame
import typing

class Spritesheet():
    def __init__(self, spritesheet_texture: pygame.Surface, padding_x: int = 0, padding_y: int = 0, cell_w: int = 16, cell_h: int = 16) -> None:
        self.spritesheet_texture = spritesheet_texture
        self.padding_x = padding_x
        self.padding_y = padding_y
        self.cell_w = cell_w
        self.cell_h = cell_h


    def get_cell(self, cell_x: int, cell_y: int) -> pygame.Surface:
        coords = self.get_cell_coords(cell_x, cell_y)
        return self.spritesheet_texture.subsurface((coords[0], coords[1], self.cell_w, self.cell_h))

    def get_cell_coords(self, cell_x: int, cell_y: int) -> tuple[int, int]:
        x = (self.cell_w * cell_x) + (cell_x * self.padding_x)
        y = (self.cell_h * cell_y) + (cell_y * self.padding_y)

        return (x, y)
    
    def fast_cell_blit_to_surface(self, cell_x: int, cell_y: int, surface: pygame.Surface, blitpos: pygame.typing.Point):
        x = (self.cell_w * cell_x) + (cell_x * self.padding_x)
        y = (self.cell_h * cell_y) + (cell_y * self.padding_y)
        
        surface.blit(self.spritesheet_texture, blitpos, area=(x, y, self.cell_w, self.cell_h))

    def all(self, xs: int, ys: int) -> list[pygame.Surface]:
        return [
            self.get_cell(x, y) for y in range(ys if ys > 0 else 1) for x in range(xs if xs > 0 else 1)
        ]

    @staticmethod
    def all_of(texture_path_to_load: str, cell_w: int, cell_h: int, xs: int, ys: int, *, padding_x: int = 0, padding_y: int = 0) -> list[pygame.Surface]:
        return Spritesheet(pygame.image.load(texture_path_to_load).convert_alpha(), padding_x, padding_y, cell_w, cell_h).all(xs, ys)