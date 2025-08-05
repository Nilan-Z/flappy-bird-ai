from flappybird.bird import Bird
class Game():
    def __init__(self, surface):
        self.bird = Bird()
        self.surface = surface

    def update(self):
        self.bird.draw(self.surface)