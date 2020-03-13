from ursina import load_texture

class Animator:
    def __init__(self, sprite, base_texture, anim_every=10, cycle=True):
        self.sprite = sprite
        self.anim_every = anim_every # how many update cycles to wait between animating frames
        self.anim_step = 0  # increments every time update() is called, used w/ anim_every 
        self.anim_frame = 1 # the current (sort of) frame of animation 
        self.base_texture = base_texture
        self.animating = True
        self.anim_dir = 1   # in what direction should the animation proceed?
                            # if 1, then go forwards; if -1, then go backwards
                            # behavior when anim_dir is not -1 or 1 is undefined.   
        self.cycle = cycle  # True: oscillates through textures (1,2,3,2,1,2,3...)
                            # False: loops through textures (1,2,3,1,2,3,1,2,3...)

        self.max_frames = 0 #the number of textures the sprite has 
        # keep on incrementing max_frames until it finds no more textures
        while load_texture(f"{self.base_texture}_{self.max_frames + 1}"):
            self.max_frames += 1

    def update(self):
        if self.animating:
            self.anim_step += 1
            # only animate after anim_step frames have passed
            if self.anim_step % self.anim_every == 0:
                self.animate()

    def animate(self):
        if self.max_frames == 0:
            return

        self.sprite.entity.texture = f"{self.base_texture}_{self.anim_frame}"

        if self.cycle: # oscillate through frames
            if self.anim_frame == self.max_frames:
                self.anim_dir = -1
            elif self.anim_frame == 1:
                self.anim_dir = 1
        else: # loop through frames
            if self.anim_frame == self.max_frames:
                self.anim_frame = 1

        # set anim_frame to the proper value for the next call to anim_dir
        self.anim_frame += self.anim_dir

    #def next_frame(self):
    #def prev_frame(self):

    def start(self):
        self.animating = True

    def stop(self):
        self.animating = False
        self.sprite.entity.texture = self.base_texture

    def kill(self):
        self.set_texture("dead")

    def set_texture(self, t):
        self.stop()
        self.sprite.entity.texture = f"{self.base_texture}_{t}"