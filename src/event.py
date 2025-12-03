import pygame
import typing
import threading
import time

class CallbackManager():
    CALLBACKS: dict[int, list[typing.Callable[[dict], typing.Any]]] = {}

    @staticmethod
    def register(id: int, op: typing.Callable[[dict], typing.Any]):
        callbacks = CallbackManager.CALLBACKS.get(id, [])
        callbacks.append(op)
        CallbackManager.CALLBACKS[id] = callbacks


def schedule(op: typing.Callable, delay: float):
    def _threadactivity(f, d):
        time.sleep(d)
        f()

    thread = threading.Thread(name="ScheduledFunction", target=_threadactivity, args=[op, delay], daemon=True)
    thread.start()

def sequence(steps: list[tuple[typing.Callable, float]]):
    def _threadactivity(s):
        for step in s:
            time.sleep(step[1])
            step[0]()

    thread = threading.Thread(name="ScheduledFunction", target=_threadactivity, args=[steps], daemon=True)
    thread.start()


PIRATE_INTERACT: int = pygame.event.custom_type()
FIRE_ITEM: int = pygame.event.custom_type()