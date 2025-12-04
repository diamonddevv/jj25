import pygame
import typing

from src import consts
from src import event
from src.render import scene
from src.render import camera
from src.render import text
from src.game import item
from src.game import ship
from src.game import pirate
from src.game import interact

class GameScene(scene.Scene):

    def __init__(self, camera: camera.Camera) -> None:
        super().__init__(camera)
        
        camera.fill_col = 0x2890dc

        self.ship = ship.Ship()
        self.items: list[item.Item] = [item.Item(0, self.ship.get_tile_center(camera, 2 + i, 4)) for i in range(10)]
        self.interactables: list[interact.Interactable] = [interact.Cannon(self.ship.get_tile_center(camera, 2 + 3*i, 1)) for i in range(10)]
        self.pirates: list[pirate.Pirate] = [pirate.NPCPirate(self.interactables, self.items, camera, self.ship, self.ship.get_tile_center(camera, 3, 3)) for _ in range(7)]

        event.CallbackManager.register(event.PICKUP_ITEM, lambda dict: self._try_pickup_callback(dict['pirate']))
        event.CallbackManager.register(event.FIRE_CANNON, lambda dict: self._fire_cannon(dict['pirate'], dict['item'], dict['cannon']))

        self.player = pirate.PlayerPirate(self.interactables, self.items, camera, self.ship, self.ship.get_tile_center(camera, 3, 3))
        self.pirates.append(self.player)

        for collider in self.ship.map_colliders:
            for p in self.pirates:
                p.track_collidable(collider)

        for c in self.interactables:
            for p in self.pirates:
                p.track_collidable_thing(c, lambda c: c.collider)


    def draw(self, camera: camera.Camera):
        super().draw(camera)
        self.ship.draw(camera)

        for pirate in self.pirates:
            pirate.draw(camera)

        for item in self.items:
            item.draw(camera)

        for cannon in self.interactables:
            cannon.draw(camera)

        # hud
        camera.with_zindex_blit(
                (
                    text.glyphxel().render_adv(f"Mateys: {len(self.pirates)}", 2),
                    pygame.Vector2(20, 20)
                ), zindex=consts.HUD_LAYER
            )

        if self.player.held_item is not None:
            camera.with_zindex_blit(
                (
                    text.glyphxel().render_adv(f"Held Item: {self.player.held_item.name()}", 2),
                    pygame.Vector2(20, 60)
                ), zindex=consts.HUD_LAYER
            )
        
        

    def update(self, dt: float, camera: camera.Camera):
        super().update(dt, camera)
        self.ship.update(dt, camera)

        camera.focus = pygame.Vector2(16 * consts.DRAW_SCALE * 16, 0)

        for pirate in self.pirates:
            pirate.update(dt, camera)

        for item in self.items:
            item.update(dt, camera)

        for cannon in self.interactables:
            cannon.update(dt, camera)


    def _try_pickup_callback(self, pirate: pirate.Pirate):
        for item in self.items:
            if pirate.held_item is None:
                if item.position.distance_squared_to(pirate.position) <= pirate.reach ** 2:
                    if item.can_be_picked_up():
                        pirate.held_item = item
                        item.held = True

    def _fire_cannon(self, pirate: pirate.Pirate, item: item.Item | None, cannon: interact.Cannon):
        if item is None:
            pirate.anim_tex.set_anim(pirate.ANIM_CROUCH + "-" + pirate.ANIM_IDLE)
        cannon.fire(item if item is not None else pirate)
        if item is not None:
            pirate.held_item = None
            event.schedule(lambda: self.items.remove(item), 5)
        else:
            def _r():
                pirate.position = pygame.Vector2(200, 200)
                pirate.fired = False
                pirate.sprite_rotation = 0.0
            event.schedule(_r, 5)

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