import pygame
import typing

class CallbackManager():
    CALLBACKS: dict[int, list[typing.Callable[[dict], typing.Any]]] = {}

    @staticmethod
    def register(id: int, op: typing.Callable[[dict], typing.Any]):
        callbacks = CallbackManager.CALLBACKS.get(id, [])
        callbacks.append(op)
        CallbackManager.CALLBACKS[id] = callbacks

PIRATE_TRY_PICKUP: int = pygame.event.custom_type()