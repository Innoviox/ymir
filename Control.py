from ursina import *


class Controller():
    def __init__(self, player):
        self.player = player
        self.app = Ursina()

    def process_input(self):
        self.velocity = None