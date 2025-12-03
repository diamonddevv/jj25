import pygame
import typing

from src import event
from src.render import scene
from src.render import camera
from src.game import item
from src.game import ship
from src.game import pirate
from src.game import interact

class GameScene(scene.Scene):

    def __init__(self, camera: camera.Camera) -> None:
        super().__init__(camera)
        
        camera.fill_col = 0x2890dc

        self.ship = ship.Ship()
        self.pirates: list[pirate.Pirate] = []
        self.items: list[item.Item] = [item.Item(i % 3, pygame.Vector2(200 + 80 * i, 400)) for i in range(10)]
        self.cannons: list[interact.Cannon] = [interact.Cannon(pygame.Vector2(600 + 100 * i, 200)) for i in range(3)]

        event.CallbackManager.register(event.PIRATE_INTERACT, lambda dict: self._try_pickup_callback(dict['pirate']))

        self.pirates.append(pirate.PlayerPirate())

        for collider in self.ship.map_colliders:
            for p in self.pirates:
                p.track_collidable(collider)

        for c in self.cannons:
            for p in self.pirates:
                p.track_collidable_thing(c, lambda c: c.collider)


    def draw(self, camera: camera.Camera):
        super().draw(camera)
        self.ship.draw(camera)

        for pirate in self.pirates:
            pirate.draw(camera)

        for item in self.items:
            item.draw(camera)

        for cannon in self.cannons:
            cannon.draw(camera)

    def update(self, dt: float, camera: camera.Camera):
        super().update(dt, camera)
        self.ship.update(dt, camera)

        for pirate in self.pirates:
            pirate.update(dt, camera)

        for item in self.items:
            if not item.held: # it is up to whatever is holding the item to draw it
                item.update(dt, camera)

        for cannon in self.cannons:
            cannon.update(dt, camera)


    def _try_pickup_callback(self, pirate: pirate.Pirate):
        for item in self.items:
            if pirate.held_item is None:
                if item.pos.distance_squared_to(pirate.position) <= pirate.pickup_distance ** 2:
                    pirate.held_item = item
                    item.held = True

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