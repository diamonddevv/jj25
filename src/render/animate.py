import pygame
import typing

from src.render import spritesheet

class AnimatedTexture():
    def __init__(self, sprsht: spritesheet.Spritesheet, anims: dict[str, tuple[int, list[tuple[int, int]]]]) -> None:
        self.sprsht = sprsht
        self.anims = anims

        self.last_anim = ''
        self.selected_anim = ''
        self.frame = 0
        self.timer = 0.0
        self.oneshot = False
        self.loop = True
        self.can_change = True

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
                if self.loop:
                    self.frame = 0
                else:
                    self.frame = len(self.anims[self.selected_anim][1]) - 1
                if self.oneshot:
                    self.selected_anim = self.last_anim
                    self.oneshot = False

    def get_frame(self) -> pygame.Surface:
        return pygame.transform.flip(self.sprsht.get_cell(*self.anims[self.selected_anim][1][min(self.frame,len(self.anims[self.selected_anim][1]) - 1)]), self.flipped, False)
    
    def set_anim(self, key: str, oneshot: bool = False, loop: bool = True):
        if key != self.selected_anim and self.can_change:
            self.last_anim = self.selected_anim
            self.selected_anim = key
            self.frame = 0
            self.timer = 0.0
            self.oneshot = oneshot
            self.loop = loop
            self.can_change = loop