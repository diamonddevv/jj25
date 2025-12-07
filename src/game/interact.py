import pygame
import random

from src import util
from src import event
from src import consts
from src.render import spritesheet
from src.render import animate
from src.render import camera
from src.game import fireable
from src.game import item
from src.game import pirate


class Interactable():
    def __init__(self, pos: pygame.Vector2 = pygame.Vector2()) -> None:
        self.position = pos
        self.collider = pygame.Rect(0, 0, 0, 0)
        self.highlight = False
        self.removal_mark = False

    def draw(self, cam: camera.Camera):
        pass

    def update(self, dt: float, cam: camera.Camera):
        pass

    def interact(self, user: pirate.Pirate):
        pass

    def can_highlight(self) -> bool:
        return True

class Cannon(Interactable):
    ANIM_IDLE: str = "idle"
    ANIM_SELECTABLE: str = "selectable"
    ANIM_FIRE: str = "firing"

    COOLDOWN: float = 12

    def __init__(self, pos: pygame.Vector2 = pygame.Vector2()) -> None:
        super().__init__(pos)
        self.spritesheet = spritesheet.Spritesheet(util.load_texture('res/interactable.png'))
        self.collider_base = pygame.Rect(0, -8, 12, 8)
        self.anim_tex = animate.AnimatedTexture(self.spritesheet,
                                                {
                                                    Cannon.ANIM_IDLE: (4, [(0, 0)]),
                                                    Cannon.ANIM_SELECTABLE: (4, [(1, 0)]),
                                                    Cannon.ANIM_FIRE: (6, [(0, 1), (1, 1), (2, 1), (3, 1)])
                                                })
        
        self.cooldown = 0.0

    def draw(self, cam: camera.Camera):
        cam.blit(
            self.anim_tex.get_frame(), self.position, scale=consts.DRAW_SCALE,zindex=-2
        )

        if self.cooldown > 0:
            cam.with_zindex(
                lambda s: pygame.draw.rect(s, 0x000000, cam.w2s_r(
                    pygame.Rect(
                        self.position - pygame.Vector2(12 * consts.DRAW_SCALE, 12 * consts.DRAW_SCALE),
                        pygame.Vector2(100, 20),
                    )
                )), zindex=-2
            )
            cam.with_zindex(
                lambda s: pygame.draw.rect(s, 0xffffff, cam.w2s_r(
                    pygame.Rect(
                        self.position - pygame.Vector2(11 * consts.DRAW_SCALE, 11 * consts.DRAW_SCALE),
                        pygame.Vector2(90, 10),
                    )
                )), zindex=-1
            )
            cam.with_zindex(
                lambda s: pygame.draw.rect(s, 0x00ff00, cam.w2s_r(
                    pygame.Rect(
                        self.position - pygame.Vector2(11 * consts.DRAW_SCALE, 11 * consts.DRAW_SCALE),
                        pygame.Vector2(90 * (self.cooldown / Cannon.COOLDOWN), 10),
                    )
                )), zindex=-1
            )

    def update(self, dt: float, cam: camera.Camera):

        if self.cooldown <= 0:
            self.anim_tex.set_anim(Cannon.ANIM_SELECTABLE if self.highlight else Cannon.ANIM_IDLE)

        if self.cooldown > 0:
            self.cooldown -= dt
        self.anim_tex.tick(dt)
        self.collider = pygame.Rect(self.position - pygame.Vector2(self.collider_base.size) * consts.DRAW_SCALE / 2 + pygame.Vector2(self.collider_base.topleft) * consts.DRAW_SCALE, pygame.Vector2(self.collider_base.size) * consts.DRAW_SCALE)

    def interact(self, user: pirate.Pirate):
        if self.cooldown <= 0:
            user.manager.fire_cannon(user, user.manager.items[user.held_item_idx] if user.held_item_idx != -1 else None, self)
            user.held_item_idx = -1

    def fire(self, firer: pirate.Pirate, fireable: fireable.Fireable):
        if self.cooldown <= 0:
            self.anim_tex.set_anim(Cannon.ANIM_FIRE, oneshot=True)
            self.anim_tex.last_anim = Cannon.ANIM_IDLE
            self.cooldown = Cannon.COOLDOWN
            event.sequence([
                (fireable.hide, 0.0),
                (fireable.show, 4/6),
                (lambda: fireable.fire(firer, self), 0.0)
            ])

    def can_highlight(self) -> bool:
        return self.cooldown <= 0

class ItemBarrel(Interactable):
    ANIM_IDLE: str = 'idle'
    ANIM_SELECTABLE: str = 'selectable'

    COOLDOWN: float = 3.0

    def __init__(self, pos: pygame.Vector2 = pygame.Vector2()) -> None:
        super().__init__(pos)
        self.spritesheet = spritesheet.Spritesheet(util.load_texture('res/interactable.png'))
        self.collider_base = pygame.Rect(0, 0, 12, 12)
        self.anim_tex = animate.AnimatedTexture(self.spritesheet,
                                                {
                                                    ItemBarrel.ANIM_IDLE: (4, [(0, 2)]),
                                                    ItemBarrel.ANIM_SELECTABLE: (4, [(1, 2)])
                                                })
        
        self.cooldown = 0.0

    def draw(self, cam: camera.Camera):
        cam.blit(
            self.anim_tex.get_frame(), self.position, scale=consts.DRAW_SCALE,zindex=-2
        )

        if self.cooldown > 0:
            cam.with_zindex(
                lambda s: pygame.draw.rect(s, 0x000000, cam.w2s_r(
                    pygame.Rect(
                        self.position - pygame.Vector2(12 * consts.DRAW_SCALE, 12 * consts.DRAW_SCALE),
                        pygame.Vector2(100, 20),
                    )
                )), zindex=-2
            )
            cam.with_zindex(
                lambda s: pygame.draw.rect(s, 0xffffff, cam.w2s_r(
                    pygame.Rect(
                        self.position - pygame.Vector2(11 * consts.DRAW_SCALE, 11 * consts.DRAW_SCALE),
                        pygame.Vector2(90, 10),
                    )
                )), zindex=-1
            )
            cam.with_zindex(
                lambda s: pygame.draw.rect(s, 0x00ff00, cam.w2s_r(
                    pygame.Rect(
                        self.position - pygame.Vector2(11 * consts.DRAW_SCALE, 11 * consts.DRAW_SCALE),
                        pygame.Vector2(90 * (self.cooldown / ItemBarrel.COOLDOWN), 10),
                    )
                )), zindex=-1
            )

    def update(self, dt: float, cam: camera.Camera):
        if self.cooldown <= 0:
            self.anim_tex.set_anim(ItemBarrel.ANIM_SELECTABLE if self.highlight else ItemBarrel.ANIM_IDLE)

        if self.cooldown > 0:
            self.cooldown -= dt
        self.anim_tex.tick(dt)
        self.collider = pygame.Rect(self.position - pygame.Vector2(self.collider_base.size) * consts.DRAW_SCALE / 2 + pygame.Vector2(self.collider_base.topleft) * consts.DRAW_SCALE, pygame.Vector2(self.collider_base.size) * consts.DRAW_SCALE)

    def interact(self, user: pirate.Pirate):
        if self.cooldown <= 0.0 and user.held_item_idx == -1:
            self.add_item(user)
            self.anim_tex.set_anim(ItemBarrel.ANIM_IDLE)
            self.cooldown = ItemBarrel.COOLDOWN

    def add_item(self, user: pirate.Pirate):
        if user.held_item_idx != -1:
            return
        
        i = item.Item(random.randint(0, len(item.Item.ITEMS) - 1))
        idx = user.manager.add_item(i)
        user.pickup_item(idx)

    def can_highlight(self) -> bool:
        return self.cooldown <= 0
    
class DamageSpot(Interactable):
        ANIM_IDLE: str = 'idle'
        ANIM_SELECTABLE: str = 'selectable'

        def __init__(self, idx: int, damage: float, pos: pygame.Vector2 = pygame.Vector2()) -> None:
            super().__init__(pos)
            self.spritesheet = spritesheet.Spritesheet(util.load_texture('res/interactable.png'))
            self.anim_tex = animate.AnimatedTexture(self.spritesheet,
                                                    {
                                                        ItemBarrel.ANIM_IDLE: (4, [(0, 3)]),
                                                        ItemBarrel.ANIM_SELECTABLE: (4, [(1, 3)])
                                                    })
            
            self.idx = idx
            self.damage = damage

        def draw(self, cam: camera.Camera):
            cam.blit(
                self.anim_tex.get_frame(), self.position, scale=consts.DRAW_SCALE,zindex=-4
            )

        def update(self, dt: float, cam: camera.Camera):
            self.anim_tex.set_anim(DamageSpot.ANIM_SELECTABLE if self.highlight else DamageSpot.ANIM_IDLE)

            self.anim_tex.tick(dt)

        def interact(self, user: pirate.Pirate):
            if user.held_item_idx != -1:
                if user.manager.items[user.held_item_idx].fixes_damage():
                    user.manager.items[user.held_item_idx].removal_mark = True
                    user.manager.interactables[self.idx].removal_mark = True
                    user.manager.boat_health += self.damage