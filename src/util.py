import pygame


def load_texture(path: str) -> pygame.Surface:
    return pygame.image.load(path).convert_alpha()


def resolve_collision(static: pygame.Rect, dynamic: pygame.Rect) -> pygame.Vector2:
    clip = dynamic.clip(static)

    left = static.x > dynamic.x
    up = static.y > dynamic.y

    prefer_hor = clip.w < clip.h

    x = clip.w * (-1 if left else 1) * (1 if prefer_hor else 0)
    y = clip.h * (-1 if up else 1) * (0 if prefer_hor else 1)

    return pygame.Vector2(x, y)