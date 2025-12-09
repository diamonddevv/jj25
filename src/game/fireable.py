import pygame
import typing

from src import consts
from src import event

if typing.TYPE_CHECKING:
    from src.game import pirate
    from src.game import interact

class Fireable():
    FIRE_SPEED: float = 400
    FIRE_ROT_SPEED: float = 360

    def __init__(self) -> None:
        self.hidden = False
        self.fired = False
        self.fired_up = True
        self.cannon_sound = pygame.mixer.Sound('res/sound/cannon.ogg')

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False
        

    def fire(self, firer: pirate.Pirate, cannon: interact.Cannon):
        self.set_position(cannon.position.copy() - pygame.Vector2(0, consts.DRAW_SCALE * 4))
        self.fired = True
        self.cannon_sound.play()

    def set_position(self, position: pygame.Vector2):
        pass