import pygame
import random

from src import consts
from src import event
from src.render import camera
from src.render import text
from src.game import pirate
from src.game import ship
from src.game import interact
from src.game import item
from src.menu import win

type _Collider = pygame.Rect | interact.Interactable

class GameManager():
    def __init__(self, cam: camera.Camera) -> None:
        self.camera = cam

        self.ship_map = ship.Ship()
        self.active_pirates: list[pirate.Pirate] = [pirate.NPCPirate(self, self.ship_map.get_tile_center(self.camera, 2 + i, 3)) for i in range(7)]
        
        self._next_item_idx: int = 0
        self.items: dict[int, item.Item] = {} 
        
        self._next_interactable_idx: int = 0
        self.interactables: dict[int, interact.Interactable] = {}
        self.add_interactables(cam)

        self.player = pirate.PlayerPirate(self, self.ship_map.get_tile_center(cam, 3, 3))
        self.active_pirates.append(self.player)

        seq = [i for i in range(10)]
        random.shuffle(seq)
        self.team_name = GameManager.resolve_team_name(seq[0], seq[1])
        self.enemy_team_name = GameManager.resolve_team_name(seq[2], seq[3])

        self.boat_health: float = 100.0
        self.enemy_health: float = 100.0

    def add_item(self, item: item.Item) -> int:
        self.items[self._next_item_idx] = item
        self._next_item_idx += 1
        return self._next_item_idx - 1

    def add_interactables(self, cam: camera.Camera):
        # cannons
        for i in range(5):
           self.interactables[self._next_interactable_idx] = interact.Cannon(self.ship_map.get_tile_center(self.camera, 5.5 + i * 5, 1)) 
           self._next_interactable_idx += 1
        
        # barrels left
        for i in range(3):
            self.interactables[self._next_interactable_idx] = interact.ItemBarrel(self.ship_map.get_tile_center(self.camera, 1, (i + 1) * 1.5)) 
            self._next_interactable_idx += 1

        # barrels right
        for i in range(3):
            self.interactables[self._next_interactable_idx] = interact.ItemBarrel(self.ship_map.get_tile_center(self.camera, 30, (i + 1) * 1.5)) 
            self._next_interactable_idx += 1


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
                    text.glyphxel().render_adv(f"{self.team_name} (Good Guys): {self.boat_health:.1f}% ship integrity", 2),
                    pygame.Vector2(consts.CANVAS_DIMS[0]/2, 25)
                ), centered=True, zindex=consts.HUD_LAYER
            )
        
        cam.with_zindex_blit(
                (
                    text.glyphxel().render_adv(f"{self.enemy_team_name} (Bad Guys): {self.enemy_health:.1f}% ship integrity", 2),
                    pygame.Vector2(consts.CANVAS_DIMS[0]/2, 65)
                ), centered=True, zindex=consts.HUD_LAYER
            )

        if self.player.held_item_idx != -1:
            cam.with_zindex_blit(
                (
                    text.glyphxel().render_adv(f"Held Item: {self.items[self.player.held_item_idx].name()}", 2),
                    pygame.Vector2(20, 20)
                ), zindex=consts.HUD_LAYER
            )

    def update(self, dt: float, cam: camera.Camera):
        self.random_enemy_fire()
        
        for pirate in self.active_pirates:
            pirate.update(dt, cam)

        r = []
        for idx in self.items:
            self.items[idx].update(dt, cam)
            if self.items[idx].position.y < -1000 or self.items[idx].position.y > 1000 + consts.CANVAS_DIMS[1]:
                self.items[idx].removal_mark = True

                if self.items[idx].fired:
                    if self.items[idx].fired_up:
                        self.enemy_health -= random.uniform(1, 5) * self.items[idx].damage_mult()
                    else:
                        self.boat_health -= random.uniform(1, 5) * self.items[idx].damage_mult()

            if self.items[idx].removal_mark:
                r.append(idx)
        for i in r:
            del self.items[i]

        for idx in self.interactables:
            self.interactables[idx].update(dt, cam)

        self.ship_map.update(dt, cam)

        if self.enemy_health <= 0.0:
            pygame.event.post(
                pygame.Event(event.CHANGE_SCENE, {
                    'scene': win.WinScene
                })
            )

        

    def fetch_all_colliders(self) -> list[_Collider]:
        return self.ship_map.map_colliders + list(self.interactables.values())
    
    def collider_rect(self, collider: _Collider) -> pygame.Rect:
        if isinstance(collider, pygame.Rect):
            return collider
        if isinstance(collider, interact.Interactable):
            return collider.collider
        return pygame.Rect(0, 0, 0, 0)

    def fire_cannon(self, firer: pirate.Pirate, item: item.Item | None, cannon: interact.Cannon):
        cannon.fire(firer, item if item is not None else firer)

    def random_enemy_fire(self):
        x = self.ship_map.get_tile_center(self.camera, random.uniform(1, 30), 0).x
        i = item.Item(random.randint(0 , len(item.Item.ITEMS) - 1), pygame.Vector2(x, 1000))
        i.fired = True
        i.fired_up = False
        self.add_item(i)

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
        