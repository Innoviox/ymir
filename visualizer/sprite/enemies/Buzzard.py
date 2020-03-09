from .BasicEnemy import BasicEnemy

class Buzzard(BasicEnemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, speed=0.2, gravity=False, hitbox=[0, 0, 1, 0.6])

        self.animator.anim_every = 10
