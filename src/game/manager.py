import pygame
import typing
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
from src.menu import lose

type _Collider = pygame.Rect | interact.Interactable

class GameManager():
    def __init__(self, cam: camera.Camera) -> None:
        self.camera = cam

        self.ship_map = ship.Ship()
        self.active_pirates: list[pirate.Pirate] = [pirate.NPCPirate(self, self.ship_map.get_tile_center(self.camera, 15 + i * (-1 if i % 2 == 0 else 1), 3)) for i in range(7)]
        
        self._next_item_idx: int = 0
        self.items: dict[int, item.Item] = {} 
        
        self._next_interactable_idx: int = 0
        self.interactables: dict[int, interact.Interactable] = {}
        self.add_interactables()

        self.player = pirate.PlayerPirate(self, self.ship_map.get_tile_center(cam, 15, 3))
        self.active_pirates.append(self.player)

        seq = [i for i in range(10)]
        random.shuffle(seq)
        self.team_name = GameManager.resolve_team_name(seq[0], seq[1])
        self.enemy_team_name = GameManager.resolve_team_name(seq[2], seq[3])

        self.boat_health: float = 100.0
        self.enemy_health: float = 100.0

        self.next_enemy_fire: float = 0.0

        self.damage_sound = pygame.mixer.Sound('res/sound/damage.ogg')

    def add_item(self, item: item.Item) -> int:
        self.items[self._next_item_idx] = item
        self._next_item_idx += 1
        return self._next_item_idx - 1
    
    def add_interactable(self, interactable: interact.Interactable):
        self.interactables[self._next_interactable_idx] = interactable
        self._next_interactable_idx += 1

    def add_interactable_idx(self, f: typing.Callable[[int], interact.Interactable]):
        self.interactables[self._next_interactable_idx] = f(self._next_interactable_idx)
        self._next_interactable_idx += 1

    def add_interactables(self):
        # cannons
        for i in range(5):
           self.add_interactable(interact.Cannon(self.ship_map.get_tile_center(self.camera, 5.5 + i * 5, 1)))
        
        # barrels left
        for i in range(3):
            self.add_interactable(interact.ItemBarrel(self.ship_map.get_tile_center(self.camera, 1, (i + 1) * 1.5)))

        # barrels right
        for i in range(3):
            self.add_interactable(interact.ItemBarrel(self.ship_map.get_tile_center(self.camera, 30, (i + 1) * 1.5)))


    def draw(self, cam: camera.Camera):
        for pirate in self.active_pirates:
            pirate.draw(cam)

        for idx in self.items:
            self.items[idx].draw(cam)

        for idx in self.interactables:
            self.interactables[idx].draw(cam)

        self.ship_map.draw(cam)

        # hud
        pos_mod = pygame.Vector2()
        if self.boat_health <= 25:
            pos_mod = pygame.Vector2(random.uniform(-5, 5), random.uniform(-5, 5))

        cam.with_zindex_blit(
                (
                    text.glyphxel().render_adv(f"{self.team_name} (Good Guys): {self.boat_health:.1f}% ship integrity", 2, color=0x005f41),
                    pygame.Vector2(consts.CANVAS_DIMS[0]/2, 25) + pos_mod
                ), centered=True, zindex=consts.HUD_LAYER
            )
        
        cam.with_zindex_blit(
                (
                    text.glyphxel().render_adv(f"{self.enemy_team_name} (Bad Guys): {self.enemy_health:.1f}% ship integrity", 2, color=0x720d0d),
                    pygame.Vector2(consts.CANVAS_DIMS[0]/2, 65)
                ), centered=True, zindex=consts.HUD_LAYER
            )
    
        self.draw_scurvy_bar(cam)
        self.draw_drunk_bar(cam)

        if self.player.held_item_idx != -1:
            cam.with_zindex_blit(
                (
                    text.glyphxel().render_adv(f"Held Item: {self.items[self.player.held_item_idx].name()}", 2),
                    pygame.Vector2(20, 20)
                ), zindex=consts.HUD_LAYER
            )
            if self.items[self.player.held_item_idx].gets_you_drunk():
                cam.with_zindex_blit(
                (
                    text.glyphxel().render_adv(f"Press E to drink", 2),
                    pygame.Vector2(20, 60)
                ), zindex=consts.HUD_LAYER
            )
            if self.items[self.player.held_item_idx].cures_scurvy():
                cam.with_zindex_blit(
                (
                    text.glyphxel().render_adv(f"Press E to eat", 2),
                    pygame.Vector2(20, 60)
                ), zindex=consts.HUD_LAYER
            )
        else:
            cam.with_zindex_blit(
                (
                    text.glyphxel().render_adv(f"Press <space> to interact", 2),
                    pygame.Vector2(20, 20)
                ), zindex=consts.HUD_LAYER
            )

    def update(self, dt: float, cam: camera.Camera):
        self.try_random_enemy_fire(dt)
        
        for pirate in self.active_pirates:
            pirate.update(dt, cam)

        r: list[int] = []
        for idx in self.items:
            self.items[idx].update(dt, cam)
            if self.items[idx].fired:
                if (self.items[idx].fired_up and self.items[idx].position.y < -600) or (not self.items[idx].fired_up and self.items[idx].position.y > 250 + (self.items[idx].random_variance - 0.5) * 180):
                    
                    if self.items[idx].causes_damage():
                        self.items[idx].removal_mark = True
                    else:
                        self.items[idx].fired = False
                        self.items[idx].rotation = 0.0

                    damage = random.uniform(1, 5) * self.items[idx].damage_mult()

                    if self.items[idx].fired_up:
                        self.enemy_health -= damage
                    else:
                        self.boat_health -= damage

                        if self.items[idx].causes_damage():
                            self.add_interactable_idx(lambda i: interact.DamageSpot(i, damage, self.items[idx].position.copy()))
                            self.damage_sound.play()

            if self.items[idx].removal_mark:
                r.append(idx)

        for i in r:
            if self.items[i].held:
                for p in self.active_pirates:
                    if p.held_item_idx == i:
                        p.held_item_idx = -1
            del self.items[i]

        r = []
        for idx in self.interactables:
            self.interactables[idx].update(dt, cam)
            if self.interactables[idx].removal_mark:
                r.append(idx)
        for i in r:
            del self.interactables[i]

        self.ship_map.update(dt, cam)

        if self.enemy_health <= 0.0:
            pygame.event.post(
                pygame.Event(event.CHANGE_SCENE, {
                    'scene': win.WinScene,
                    'ctx': ()
                })
            )

        if self.boat_health <= 0.0:
            pygame.event.post(
                pygame.Event(event.CHANGE_SCENE, {
                    'scene': lose.LoseScene,
                    'ctx': [False]
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

    def try_random_enemy_fire(self, dt: float):
        self.next_enemy_fire -= dt

        if self.next_enemy_fire <= 0:    
            x = self.ship_map.get_tile_center(self.camera, random.uniform(1, 30), 0).x
            i = item.Item(random.randint(0 , len(item.Item.ITEMS) - 1), pygame.Vector2(x, -800))
            i.fired = True
            i.fired_up = False
            self.add_item(i)
            self.next_enemy_fire = random.uniform(0.5, 4)

    def draw_scurvy_bar(self, cam: camera.Camera):
        pos_mod = pygame.Vector2()
        if self.player.scurvy_time <= pirate.Pirate.SCURVY_WARNING_TIME:
            pos_mod = pygame.Vector2(random.uniform(-5, 5), random.uniform(-5, 5))

        cam.with_zindex(
                lambda s: pygame.draw.rect(s, 0x000000,
                    pygame.Rect(
                        pygame.Vector2(consts.CANVAS_DIMS[0] - 220, 20) + pos_mod,
                        pygame.Vector2(200, 20),
                    )
                ), zindex=consts.HUD_LAYER
            )
        cam.with_zindex(
                lambda s: s.blit(text.glyphxel().render_adv('Scurvy-o-meter: ', 2, 0x0),
                                 pygame.Vector2(consts.CANVAS_DIMS[0] - 470, 8) + pos_mod), zindex=consts.HUD_LAYER
            )
        cam.with_zindex(
            lambda s: pygame.draw.rect(s, 0xffffff,
                pygame.Rect(
                        pygame.Vector2(consts.CANVAS_DIMS[0] - 215, 25) + pos_mod,
                        pygame.Vector2(190, 10),
                    )
            ), zindex=consts.HUD_LAYER
        )
        cam.with_zindex(
            lambda s: pygame.draw.rect(s, 0xecab11,
                pygame.Rect(
                        pygame.Vector2(consts.CANVAS_DIMS[0] - 215, 25) + pos_mod,
                        pygame.Vector2(190 * (self.player.scurvy_time / pirate.Pirate.SCURVY_TIME), 10),
                    )
            ), zindex=consts.HUD_LAYER
        )

    def draw_drunk_bar(self, cam: camera.Camera):

        cam.with_zindex(
                lambda s: pygame.draw.rect(s, 0x000000,
                    pygame.Rect(
                        pygame.Vector2(consts.CANVAS_DIMS[0] - 220, 80),
                        pygame.Vector2(200, 20),
                    )
                ), zindex=consts.HUD_LAYER
            )
        cam.with_zindex(
                lambda s: s.blit(text.glyphxel().render_adv('Drunk-o-meter: ', 2, 0x0),
                                 pygame.Vector2(consts.CANVAS_DIMS[0] - 455, 68)), zindex=consts.HUD_LAYER
            )
        cam.with_zindex(
            lambda s: pygame.draw.rect(s, 0xffffff,
                pygame.Rect(
                        pygame.Vector2(consts.CANVAS_DIMS[0] - 215, 85),
                        pygame.Vector2(190, 10),
                    )
            ), zindex=consts.HUD_LAYER
        )
        cam.with_zindex(
            lambda s: pygame.draw.rect(s, 0xc12458,
                pygame.Rect(
                        pygame.Vector2(consts.CANVAS_DIMS[0] - 215, 85),
                        pygame.Vector2(190 * (self.player.drunk_time / pirate.Pirate.MAX_DRUNK_TIME), 10),
                    )
            ), zindex=consts.HUD_LAYER
        )

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
        