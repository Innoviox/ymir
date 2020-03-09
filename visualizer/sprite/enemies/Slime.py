from .BasicEnemy import BasicEnemy

class Slime(BasicEnemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, speed=-0.2, hitbox= [0, 0, 1, 0.7])