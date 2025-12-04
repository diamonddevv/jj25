from __future__ import annotations
import pygame
import random
import typing

from src.render import camera

type _TaskProvider[T] = type[Task[T]]

class Brain[T]():

    def __init__(self) -> None:
        self.task_pool: list[_TaskProvider[T]] = []

        self.task: Task | None = None

    def add_task(self, task_provider: _TaskProvider[T], weight: int = 1):
        for _ in range(weight):
            self.task_pool.append(task_provider)

    def update(self, dt: float, cam: camera.Camera, t: T):
        if self.task is None or (self.task.can_finish(t) or self.task.age > 20):
            self.pick_task(t)
        if self.task is not None:
            self.task.process(dt, cam, t)


    def pick_task(self, t: T):
        task_found = False
        while not task_found:
            proposed_task = random.choice(self.task_pool)(t)
            if proposed_task.prereq(t):
                task_found = True
                self.task = proposed_task
                self.task.start(t)


class Task[T]():
    def __init__(self) -> None:
        self.age = 0.0

    def prereq(self, t: T) -> bool:
        return True
    
    def can_finish(self, t: T) -> bool:
        return self.age > random.uniform(2.0, 5.0)
    
    def start(self, t: T):
        pass
    
    def process(self, dt: float, cam: camera.Camera, t: T):
        self.age += dt