import pygame
import random

class Pipe():
    def __init__(self, x):
        self.pipe_image = pygame.image.load("assets/sprites/pipe-green.png").convert_alpha()
        self.flipped_pipe = pygame.transform.flip(self.pipe_image, False, True)
        self.gap = 120
        self.velocity = 2
        self.x = x
        self.passed = False
        self.width = self.pipe_image.get_width()
        self.set_height()

    def set_height(self):
        height = random.randint(50, 300)
        self.top_y = height - self.pipe_image.get_height()
        self.bottom_y = height + self.gap

    def update(self):
        self.x -= self.velocity

    def draw(self, surface):
        surface.blit(self.flipped_pipe, (self.x, self.top_y))
        surface.blit(self.pipe_image, (self.x, self.bottom_y))

    def get_rects(self):
        top_rect = pygame.Rect(self.x, self.top_y, self.pipe_image.get_width(), self.pipe_image.get_height())
        bottom_rect = pygame.Rect(self.x, self.bottom_y, self.pipe_image.get_width(), self.pipe_image.get_height())
        return top_rect, bottom_rect
