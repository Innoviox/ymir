import numpy as np

from visualizer.sprite import Sprite
from visualizer.util import *
from math import sqrt
from abc import ABC, abstractmethod

class Enemy(Sprite,ABC):
    @abstractmethod
    def update(self,dt):
        super().update(dt)
