import pygame

from src import consts
from src import event

class Fireable():
    FIRE_SPEED: float = 400
    FIRE_ROT_SPEED: float = 360

    def __init__(self) -> None:
        self.hidden = False
        self.fired = False
        self.fired_up = True

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def _start_fire_anim(self, position: pygame.Vector2):
        self.set_position(position.copy() - pygame.Vector2(0, consts.DRAW_SCALE * 4))
        self.fired = True

    def set_position(self, position: pygame.Vector2):
        pass