import pygame

from src import util
from src import event
from src import consts
from src.render import scene
from src.render import camera
from src.render import spritesheet
from src.render import text

class Window():
    def __init__(self, default_scene: type[scene.Scene]) -> None:
        self.window = pygame.window.Window(
            title=consts.TITLE,
            size=consts.WINDOW_DIMS,
            resizable=True
        )

        self.window_surface = self.window.get_surface()
        self.canvas = pygame.Surface(consts.CANVAS_DIMS)

        self.clock = pygame.Clock()
        self.keep_open = False

        self.camera = camera.Camera(self.window)
        self.scene_manager = scene.SceneManager(self.camera, default_scene, ())

        pygame.mixer.music.load('res/sound/pirate-plunder.ogg')
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)

        event.CallbackManager.register(event.CHANGE_SCENE, lambda d: self.scene_manager.change(self.camera, d['scene'], d['ctx']))

        player_spr = spritesheet.Spritesheet(util.load_texture('res/pirate.png'))
        c = player_spr.get_cell(1, 1)
        self.window.set_icon(c)

        #
        """
        surface = pygame.Surface((630, 500))

        
        ship_spr = spritesheet.Spritesheet(util.load_texture('res/ship.png'))
        for x in range(100):
            for y in range(100):
                c = ship_spr.get_cell(0, 0)
                surface.blit(
                    pygame.transform.scale_by(c, 8), (x * 16 * 8, y * 16 * 8)
                )
        


        ddv = util.load_texture('res/ddv.png')
        surface.blit(
            pygame.transform.scale_by(ddv, 0.1), 
            (
                20, 20
            )
        )

        t = text.sfsans().render_adv("cap' itulate", 3, 0x00)
        surface.blit(t, pygame.Vector2(
            surface.width / 2 - t.width / 2 - 4,
            surface.height / 2 - t.height / 2 + 4,
        ))
        t = text.sfsans().render_adv("cap' itulate", 3)
        surface.blit(t, pygame.Vector2(
            surface.width / 2 - t.width / 2,
            surface.height / 2 - t.height / 2,
        ))
        pygame.image.save(
            surface, 'promo/banner.png'
        )
        """

    def init_resources(self):
        text.PixelFont.init_pixelfonts()

    def start(self):
        self.keep_open = True
        dt = 0.0

        while self.keep_open:
            self.event(dt)
            self.update(dt)
            self.draw(self.canvas)
            
            self.window_surface.blit(pygame.transform.scale(self.canvas, self.window_surface.size))

            self.window.flip()
            dt = self.clock.tick(consts.TARGET_FRAMERATE) / 1000

            self.window.title = f"{consts.TITLE} | FPS: {self.clock.get_fps():.0f}"


    def draw(self, cvs: pygame.Surface):
        cvs.fill(0x0)
        self.scene_manager.draw_current(self.camera)
        self.camera.render(self.canvas)

    def update(self, dt: float):
        self.scene_manager.update_current(dt, self.camera)

    def event(self, dt: float):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.keep_open = False

            if e.type in event.CallbackManager.CALLBACKS:
                for o in event.CallbackManager.CALLBACKS[e.type]:
                    o(e.dict)