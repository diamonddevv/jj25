import pygame


def load_texture(path: str) -> pygame.Surface:
    return pygame.image.load(path).convert_alpha()