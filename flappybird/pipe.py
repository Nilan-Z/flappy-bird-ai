import pygame
import random

class Pipe():
    def __init__(self, x):
        self.original_sprite = pygame.image.load("assets/sprites/pipe-green.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.original_sprite, (int(self.original_sprite.get_width() * 1.5), int(self.original_sprite.get_height())))
        self.flipped_sprite = pygame.transform.flip(self.sprite, False, True)
        self.gap = 150
        self.velocity = 3
        self.x = x
        self.passed = False
        self.width = self.sprite.get_width()
        self.set_height()

    def set_height(self):
        height = random.randint(50, 300)
        self.top_y = height - self.sprite.get_height()
        self.bottom_y = height + self.gap

    def update(self):
        self.x -= self.velocity

    def draw(self, surface):
        surface.blit(self.flipped_sprite, (self.x, self.top_y))
        surface.blit(self.sprite, (self.x, self.bottom_y))

    def get_rects(self):
        top_rect = pygame.Rect(self.x, self.top_y, self.sprite.get_width(), self.sprite.get_height())
        bottom_rect = pygame.Rect(self.x, self.bottom_y, self.sprite.get_width(), self.sprite.get_height())
        return top_rect, bottom_rect
