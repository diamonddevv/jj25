import pygame
import typing

from src.render import spritesheet

class AnimatedTexture():
    def __init__(self, sprsht: spritesheet.Spritesheet, anims: dict[str, tuple[int, list[tuple[int, int]]]]) -> None:
        self.sprsht = sprsht
        self.anims = anims

        self.selected_anim = ''
        self.frame = 0
        self.timer = 0.0

        self.flipped = False

        for key in self.anims.keys():
            self.selected_anim = key
            break

    def tick(self, dt: float):
        spf = 1/self.anims[self.selected_anim][0]
        self.timer += dt

        if self.timer >= spf:
            self.timer = 0.0
            self.frame += 1
            if self.frame >= len(self.anims[self.selected_anim][1]):
                self.frame = 0

    def get_frame(self) -> pygame.Surface:
        return pygame.transform.flip(self.sprsht.get_cell(*self.anims[self.selected_anim][1][self.frame]), self.flipped, False)
    
    def set_anim(self, key: str):
        if key != self.selected_anim:
            self.selected_anim = key
            self.frame = 0
            self.timer = 0.0