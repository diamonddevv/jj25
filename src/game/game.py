import pygame
import typing

from src.render import scene
from src.render import camera
from src.render import text

from src.game import ship
from src.game import pirate

class GameScene(scene.Scene):

    def __init__(self, camera: camera.Camera) -> None:
        super().__init__(camera)
        
        camera.fill_col = 0xFFFFFF

        self.ship = ship.Ship()

        self.pirates: list[pirate.Pirate] = []
        self.pirates.append(pirate.PlayerPirate())

        self.rect = pygame.Rect(0, 0, 100, 100)

        for p in self.pirates:
            p.track_collidable(self.rect)

    def draw(self, camera: camera.Camera):
        super().draw(camera)
        self.ship.draw(camera)

        for pirate in self.pirates:
            pirate.draw(camera)

        camera.with_zindex(lambda s: pygame.draw.rect(s, 'blue', camera.w2s_r(self.rect)))

    def update(self, dt: float, camera: camera.Camera):
        super().update(dt, camera)
        self.ship.update(dt, camera)

        for pirate in self.pirates:
            pirate.update(dt, camera)

    @staticmethod
    def resolve_team_name(prefix: int, suffix: int) -> str:
        pre = ''
        suf = ''

        match prefix:
            case 0: pre = "Landlubbin'"
            case 1: pre = "Swashbucklin'"
            case 2: pre = "Buccaneerin'"
            case 3: pre = "Plunderin'"
            case 4: pre = "Pillagin'"
            case 5: pre = "Ahoy!"
            case 6: pre = "Arr!"
            case 7: pre = "Rum-Lovin'"
            case 8: pre = "Bounty-Lovin'"
            case 9: pre = "Parrot-Lovin'"
            case _: pre = ""

        match suffix:
            case 0: suf = "Landlubbers"
            case 1: suf = "Swashbucklers"
            case 2: suf = "Buccaneers"
            case 3: suf = "Plunderers"
            case 4: suf = "Pillagers"
            case 5: suf = "Mateys"
            case 6: suf = "Scurvy Dogs"
            case 7: suf = "Rum Gang"
            case 8: suf = "Bounty Gang"
            case 9: suf = "Parrot Gang"
            case _: suf = ""

        return f"{pre} {suf}"