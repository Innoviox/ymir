from visualizer.sprite.sprite import Sprite
from abc import ABC, abstractmethod

class Enemy(Sprite, ABC):
    @abstractmethod
    def update(self, dt):
        super().update(dt)
