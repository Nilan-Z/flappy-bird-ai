import pygame
from flappybird.bird import Bird

class Game():
    def __init__(self, surface):
        self.bird = Bird()
        self.surface = surface
        self.base = pygame.image.load("assets/sprites/base.png").convert_alpha()
        self.velocity = 0
        self.base_x = 0
        self.base_scroll_speed = 3
        self.base_width = self.base.get_width()
        self.screen_width = surface.get_width()
        self.screen_height = surface.get_height()


    def update(self):
        self.bird.draw(self.surface)
        self.base_x -= self.base_scroll_speed
        if self.base_x <= -self.base_width:
            self.base_x = 0
        self.surface.blit(self.base, (self.base_x, self.screen_height - self.base.get_height() / 1.7))
        self.surface.blit(self.base, (self.base_x + self.base_width, self.screen_height - self.base.get_height() / 1.7))