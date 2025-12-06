from __future__ import annotations
import pygame
import random
import typing

from src import util
from src import consts
from src import event
from src.render import spritesheet
from src.render import camera
from src.render import animate
from src.game import item
from src.game import interact
from src.game import fireable
from src.game import brain
from src.game import ship

from src.game import manager

class Pirate(fireable.Fireable):
    ANIM_IDLE: str = 'idle'
    ANIM_RUN: str = 'run'
    ANIM_CROUCH: str = 'crouch'
    ANIM_HOLD: str = 'hold'

    def __init__(self, manager: manager.GameManager, pos: pygame.Vector2) -> None:
        super().__init__()
        self.position = pos
        self.speed = 300.0
        self.sprite_rotation = 0.0
        self.reach = 80
        self.crouched = False
        self.update_anim = True
        self.held_item_idx: int = -1
        self.collision_box = pygame.Rect(0, 0, 0, 0)

        self.manager = manager

        self.anim_tex = animate.AnimatedTexture(spritesheet.Spritesheet(util.load_texture('res/pirate.png')), {
            Pirate.ANIM_IDLE: (5, [(0, 0), (1, 0)]),
            Pirate.ANIM_RUN: (5, [(0, 1), (1, 1)]),
            Pirate.ANIM_CROUCH + "-" + Pirate.ANIM_IDLE: (5, [(2, 0)]),
            Pirate.ANIM_CROUCH + "-" + Pirate.ANIM_RUN: (5, [(2, 1), (3, 1)]),

            Pirate.ANIM_IDLE + "-" + Pirate.ANIM_HOLD: (5, [(0, 3)]),
            Pirate.ANIM_RUN + "-" + Pirate.ANIM_HOLD: (5, [(0, 3), (1, 3)]),
            Pirate.ANIM_CROUCH + "-" + Pirate.ANIM_IDLE + "-" + Pirate.ANIM_HOLD: (5, [(0, 3)]),
            Pirate.ANIM_CROUCH + "-" + Pirate.ANIM_RUN + "-" + Pirate.ANIM_HOLD: (5, [(0, 3), (1, 3)])
        })

    def draw(self, cam: camera.Camera):
        if self.hidden:
            return

        cam.blit(
            self.anim_tex.get_frame(),
            self.position, True, scale=consts.DRAW_SCALE,
            rotation=self.sprite_rotation
        )

        if consts.DRAW_COLLISION_BOXES:
            cam.with_zindex(lambda s: pygame.draw.rect(s, 'red', cam.w2s_r(self.collision_box), 8), 10)

        if self.held_item_idx != -1:
            self.manager.items[self.held_item_idx].flip_texture = self.anim_tex.flipped
            self.manager.items[self.held_item_idx].position = self.position + pygame.Vector2(8 * (-1 if self.anim_tex.flipped else 1), -8 * consts.DRAW_SCALE)

    def update(self, dt: float, cam: camera.Camera):
        if self.hidden:
            return
        
        self.anim_tex.tick(dt)

        if self.fired:
            self.position.y -= fireable.Fireable.FIRE_SPEED * dt * (1 if self.fired_up else -1)
            self.sprite_rotation += fireable.Fireable.FIRE_ROT_SPEED * dt
        else:
            movement = self.get_movement(dt)

            anim = Pirate.ANIM_IDLE
            if movement != pygame.Vector2():
                anim = Pirate.ANIM_RUN

            if self.crouched:
                anim = Pirate.ANIM_CROUCH + "-" + anim

            if self.held_item_idx != -1:
                anim = anim + "-" + Pirate.ANIM_HOLD

            if self.update_anim:
                self.anim_tex.set_anim(anim)
        
            if movement.x != 0:
                self.anim_tex.flipped = movement.x < 0

            self.collision_box = self.anim_tex.get_frame().get_rect(center=self.position).scale_by(consts.DRAW_SCALE)

            self.position += movement.elementwise() * dt * self.speed * (0.6 if self.crouched or self.held_item_idx != -1 else 1)

            if self.manager is not None:
                for collider in self.manager.fetch_all_colliders():
                    rect = self.manager.collider_rect(collider)
                    if pygame.Vector2(rect.center).distance_squared_to(self.position) < 20000:
                        resolution = util.resolve_collision(rect, self.collision_box)
                        self.position += resolution
                

    def get_movement(self, dt: float) -> pygame.Vector2:
        return pygame.Vector2()
    
    def set_position(self, position: pygame.Vector2):
        self.position = position

    def closest_interactable_idx(self) -> int:
        if len(self.manager.interactables) <= 0:
            return -1
        return sorted(self.manager.interactables, key=lambda idx: self.position.distance_squared_to(self.manager.interactables[idx].position))[0]
    
    def fire(self, firer: Pirate, cannon: interact.Cannon):
        super().fire(firer, cannon)
        self.anim_tex.set_anim(Pirate.ANIM_CROUCH + "-" + Pirate.ANIM_IDLE)
        def _r():
                firer.position = pygame.Vector2(200, 200)
                firer.fired = False
                firer.sprite_rotation = 0.0
        event.schedule(_r, 5)

    def pickup_item(self, item_idx: int):
        self.held_item_idx = item_idx
        self.manager.items[self.held_item_idx].held = True

class PlayerPirate(Pirate):

    KEY_UP: int = pygame.K_w
    KEY_DOWN: int = pygame.K_s
    KEY_LEFT: int = pygame.K_a
    KEY_RIGHT: int = pygame.K_d
    KEY_CROUCH: int = pygame.K_LSHIFT
    KEY_INTERACT: int = pygame.K_SPACE

    def __init__(self, manager: manager.GameManager, pos: pygame.Vector2) -> None:
        super().__init__(manager, pos)

        self.arrow = animate.AnimatedTexture(
            spritesheet.Spritesheet(util.load_texture('res/pirate.png')),
            {
                '': (4, [(0, 4), (1, 4)])
            })

    def get_movement(self, dt: float) -> pygame.Vector2:
        keys = pygame.key.get_pressed()
        vec = pygame.Vector2()

        if keys[PlayerPirate.KEY_UP]: vec.y -= 1
        if keys[PlayerPirate.KEY_LEFT]: vec.x -= 1
        if keys[PlayerPirate.KEY_DOWN]: vec.y += 1
        if keys[PlayerPirate.KEY_RIGHT]: vec.x += 1

        self.crouched = keys[PlayerPirate.KEY_CROUCH]

        if vec.length() != 0:
            vec.normalize_ip()

        return vec
    
    def draw(self, cam: camera.Camera):
        super().draw(cam)

        if not self.hidden:
            cam.blit(self.arrow.get_frame(), self.position - pygame.Vector2(0, 48 if self.held_item_idx == -1 else 72), scale=consts.DRAW_SCALE, zindex=5)

        # colliders
        if consts.DRAW_COLLISION_BOXES:
            for collider in self.manager.fetch_all_colliders():
                cam.with_zindex_provider(lambda s, r: pygame.draw.rect(s, 'green', cam.w2s_r(r), 8), self.manager.collider_rect(collider), 10)
    
    def update(self, dt: float, cam: camera.Camera):
        super().update(dt, cam)

        self.arrow.tick(dt)

        pressed_interact = pygame.key.get_just_pressed()[PlayerPirate.KEY_INTERACT]

        for idx in self.manager.interactables:
            self.manager.interactables[idx].highlight = False
        closest = self.closest_interactable_idx()
        if closest != -1 and self.position.distance_squared_to(self.manager.interactables[closest].position) <= self.reach ** 2 and self.manager.interactables[closest].can_highlight():
            self.manager.interactables[closest].highlight = True

        if pressed_interact:
            picked_up_item = False
            if self.held_item_idx == -1:
                for idx in self.manager.items:
                    if self.position.distance_squared_to(self.manager.items[idx].position) <= self.reach ** 2:
                        if self.manager.items[idx].can_be_picked_up():
                            picked_up_item = True
                            self.pickup_item(idx)
                            break

            if not picked_up_item:
                if closest != -1 and self.manager.interactables[closest].highlight:
                    cl = self.manager.interactables[closest]
                    cl.interact(self)
                elif self.held_item_idx != -1:
                    self.manager.items[self.held_item_idx].held = False
                    self.manager.items[self.held_item_idx].position = self.position.copy()
                    self.held_item_idx = -1

class NPCPirate(Pirate):
    def __init__(self, manager: manager.GameManager, pos: pygame.Vector2) -> None:
        super().__init__(manager, pos)

        self.brain = PirateBrain()
        self.target_position = self.position
        self.target_pos_tolerance = 8
        self.at_target = False

    def update(self, dt: float, cam: camera.Camera):
        super().update(dt, cam)
        self.brain.update(dt, cam, self)
        self.at_target = self.position.distance_squared_to(self.target_position) <= self.target_pos_tolerance ** 2

    def get_movement(self, dt: float) -> pygame.Vector2:
        super().get_movement(dt)

        if not self.at_target:
            dist = (self.target_position - self.position)
            if dist.length() != 0:
                return dist.normalize()
        return pygame.Vector2(0,0)
    


class PirateBrain(brain.Brain[NPCPirate]):
    def __init__(self) -> None:
        super().__init__()


        self.add_task(WalkToPositionTask, 5)
        self.add_task(FindItemTask, 1)
        self.add_task(PickUpItemTask, 1)
        self.add_task(FireCannonTask, 1)

class WalkToPositionTask(brain.Task[NPCPirate]):
    def __init__(self) -> None:
        super().__init__()
        self.target = pygame.Vector2()

    def start(self, t: NPCPirate):
        tl = t.manager.ship_map.get_tile_center(t.manager.camera, 1, 1)
        br = t.manager.ship_map.get_tile_center(t.manager.camera, 30, 5)

        self.target = pygame.Vector2(
                random.uniform(tl.x, br.x),
                random.uniform(tl.y, br.y)
            )

    def process(self, dt: float, cam: camera.Camera, t: NPCPirate):
        super().process(dt, cam, t)
        t.target_position = self.target.copy()

class FindItemTask(brain.Task[NPCPirate]):
    def __init__(self) -> None:
        super().__init__()

        self.target: int = -1
        
    
    def start(self, t: NPCPirate):
        l = list(filter(lambda idx: isinstance(t.manager.interactables[idx], interact.ItemBarrel), t.manager.interactables.keys()))
        if len(l) <= 0:
            return
        self.target = l[random.randint(0, len(l) - 1)]

    def process(self, dt: float, cam: camera.Camera, t: NPCPirate):
        super().process(dt, cam, t)
        t.target_position = t.manager.interactables[self.target].position.copy()

        if t.position.distance_squared_to(t.manager.interactables[self.target].position) <= t.reach ** 2 and t.held_item_idx == -1:
            cl = t.manager.interactables[self.target]
            if isinstance(cl, interact.ItemBarrel):
                if cl.cooldown <= 0:
                    cl.add_item(t)
    
    def can_finish(self, t: NPCPirate) -> bool:
        return t.held_item_idx != -1

    def prereq(self, t: NPCPirate) -> bool:
        return t.held_item_idx == -1 and len(t.manager.interactables) > 0

class PickUpItemTask(brain.Task[NPCPirate]):
    def __init__(self) -> None:
        super().__init__()
        self.target: int = -1
        

    def start(self, t: NPCPirate):
        l = list(filter(lambda idx: t.manager.items[idx].can_be_picked_up(), t.manager.items.keys()))
        if len(l) <= 0:
            return
        self.target = l[random.randint(0, len(l) - 1)]

    def process(self, dt: float, cam: camera.Camera, t: NPCPirate):
        super().process(dt, cam, t)
        if self.target != -1:
            t.target_position = t.manager.items[self.target].position.copy()

            if t.position.distance_squared_to(t.manager.items[self.target].position) <= t.reach ** 2 and t.manager.items[self.target].can_be_picked_up(): 
                t.pickup_item(self.target)
    
    def prereq(self, t: NPCPirate) -> bool:
        return len(t.manager.items) > 0 and t.held_item_idx == -1

    def can_finish(self, t: NPCPirate) -> bool:
        return self.target == -1 or not t.manager.items[self.target].can_be_picked_up()

class FireCannonTask(brain.Task[NPCPirate]):
    def __init__(self) -> None:
        super().__init__()

        self.target: int = -1
        
    
    def start(self, t: NPCPirate):
        l = list(filter(lambda idx: isinstance(t.manager.interactables[idx], interact.Cannon), t.manager.interactables.keys()))
        if len(l) <= 0:
            return
        self.target = l[random.randint(0, len(l) - 1)]

    def process(self, dt: float, cam: camera.Camera, t: NPCPirate):
        super().process(dt, cam, t)
        t.target_position = t.manager.interactables[self.target].position.copy()

        if t.position.distance_squared_to(t.manager.interactables[self.target].position) <= t.reach ** 2 and t.held_item_idx != -1:
            cl = t.manager.interactables[self.target]
            if isinstance(cl, interact.Cannon):
                if cl.cooldown <= 0:
                    t.manager.fire_cannon(t, t.manager.items[t.held_item_idx], cl)
                    t.held_item_idx = -1
    
    def can_finish(self, t: NPCPirate) -> bool:
        c = t.manager.interactables[self.target]
        assert isinstance(c, interact.Cannon)
        return t.held_item_idx == -1 or c.cooldown > 0

    def prereq(self, t: NPCPirate) -> bool:
        return t.held_item_idx != -1 and len(t.manager.interactables) > 0