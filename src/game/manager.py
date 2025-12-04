import pygame

from src import consts
from src import event
from src.render import camera
from src.render import text
from src.game import pirate
from src.game import ship
from src.game import interact
from src.game import item

type _Collider = pygame.Rect | interact.Interactable

class GameManager():
    def __init__(self, cam: camera.Camera) -> None:
        self.camera = cam

        self.ship_map = ship.Ship()
        self.active_pirates: list[pirate.Pirate] = []
        self.items: dict[int, item.Item] = {i: item.Item(0, self.ship_map.get_tile_center(self.camera, 2 + i, 3)) for i in range(5)}
        self.interactables: dict[int, interact.Interactable] = {i: interact.Cannon(self.ship_map.get_tile_center(self.camera, 2 + i, 1)) for i in range(5)}

        self.player = pirate.PlayerPirate(self, self.ship_map.get_tile_center(cam, 3, 3))
        self.active_pirates.append(self.player)


    def draw(self, cam: camera.Camera):
        for pirate in self.active_pirates:
            pirate.draw(cam)

        for idx in self.items:
            self.items[idx].draw(cam)

        for idx in self.interactables:
            self.interactables[idx].draw(cam)

        self.ship_map.draw(cam)

        # hud
        cam.with_zindex_blit(
                (
                    text.glyphxel().render_adv(f"Mateys: {len(self.active_pirates)}", 2),
                    pygame.Vector2(20, 20)
                ), zindex=consts.HUD_LAYER
            )

        if self.player.held_item_idx != -1:
            cam.with_zindex_blit(
                (
                    text.glyphxel().render_adv(f"Held Item: {self.items[self.player.held_item_idx].name()}", 2),
                    pygame.Vector2(20, 60)
                ), zindex=consts.HUD_LAYER
            )

    def update(self, dt: float, cam: camera.Camera):
        for pirate in self.active_pirates:
            pirate.update(dt, cam)

        for idx in self.items:
            self.items[idx].update(dt, cam)

        for idx in self.interactables:
            self.interactables[idx].update(dt, cam)

        self.ship_map.update(dt, cam)

    def fetch_all_colliders(self) -> list[_Collider]:
        return self.ship_map.map_colliders + list(self.interactables.values())
    
    def collider_rect(self, collider: _Collider) -> pygame.Rect:
        if isinstance(collider, pygame.Rect):
            return collider
        if isinstance(collider, interact.Interactable):
            return collider.collider
        return pygame.Rect(0, 0, 0, 0)


    def pickup_item(self, pickerupper: pirate.Pirate, item_id: int):
        item = self.items[item_id]
        pass

    def fire_cannon(self, firer: pirate.Pirate, item: item.Item | None, cannon: interact.Cannon):
        cannon.fire(firer, item if item is not None else firer)
        