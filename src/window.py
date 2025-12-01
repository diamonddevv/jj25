import pygame

from src import util
from src import consts
from src import shared
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

        self.scene_manager = scene.SceneManager(default_scene)
        self.camera = camera.Camera()

    def init_resources(self):
        text.PixelFont.init_pixelfonts()
        shared.SPRITESHEET = spritesheet.Spritesheet(util.load_texture('res/sprites.png'))

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