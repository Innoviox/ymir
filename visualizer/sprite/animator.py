from ursina import load_texture

class Animator:
    def __init__(self, sprite, base_texture, anim_every=10, cycle=True):
        self.sprite = sprite
        self.anim_every = anim_every # loop cycle
        self.anim_step = 0
        self.anim_frame = 1
        self.base_texture = base_texture
        self.animating = True
        self.anim_dir = 1
        self.cycle = cycle  # True: oscillates through textures (1,2,3,2,1,2,3...)
                            # False: loops through textures (1,2,3,1,2,3,1,2,3...)

        self.max_frames = 0
        while load_texture(f"{self.base_texture}_{self.max_frames + 1}"):
            self.max_frames += 1

    def update(self):
        if self.animating:
            self.anim_step += 1
            if self.anim_step % self.anim_every == 0:
                self.animate()

    def animate(self):
        if self.max_frames == 0:
            return

        self.sprite.entity.texture = f"{self.base_texture}_{self.anim_frame}"

        if self.cycle:
            if self.anim_frame == self.max_frames:
                self.anim_dir = -1
            elif self.anim_frame == 1:
                self.anim_dir = 1
        else:
            if self.anim_frame == self.max_frames:
                self.anim_frame = 1

        self.anim_frame += self.anim_dir

    def start(self):
        self.animating = True

    def stop(self):
        self.animating = False

    def kill(self):
        self.stop()
        self.sprite.entity.texture = f"{self.base_texture}_dead"