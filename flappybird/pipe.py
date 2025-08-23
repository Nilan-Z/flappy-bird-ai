import pygame
import random
import yaml

class Pipe():
    def __init__(self, x):
        """
        Initialize a Pipe object at a given horizontal position.
        
        Args:
            x (int): The initial x-coordinate of the pipe on the screen.
        """
        with open("config.yaml", "r") as f:
            cfg = yaml.safe_load(f)

        self.original_sprite = pygame.image.load("assets/sprites/pipe-green.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.original_sprite, (int(self.original_sprite.get_width() * 1.5), int(self.original_sprite.get_height())))
        self.flipped_sprite = pygame.transform.flip(self.sprite, False, True)
        self.gap = int(cfg.get("pipe_gap", 100))
        self.velocity = 3
        self.x = x
        self.passed = False
        self.width = self.sprite.get_width()
        self.set_height()

    def set_height(self):
        """
        Randomly set the vertical position of the pipe pair.

        The top pipe's position is calculated to be off-screen upwards by
        subtracting its height from a random height value.
        The bottom pipe is positioned below the gap.
        """
        height = random.randint(50, 300)
        self.top_y = height - self.sprite.get_height()
        self.bottom_y = height + self.gap

    def update(self):
        """
        Update the pipe's horizontal position by moving it leftwards
        according to its velocity.
        """
        self.x -= self.velocity

    def draw(self, surface):
        """
        Draw both the top and bottom pipes on the given surface.

        Args:
            surface (pygame.Surface): The surface to render the pipes on.
        """
        surface.blit(self.flipped_sprite, (self.x, self.top_y))
        surface.blit(self.sprite, (self.x, self.bottom_y))

    def get_rects(self):
        """
        Get the collision rectangles for the top and bottom pipes.

        Returns:
            tuple: Two pygame.Rect objects representing the bounding boxes of
                   the top and bottom pipes respectively.
        """
        top_rect = pygame.Rect(self.x, self.top_y, self.sprite.get_width(), self.sprite.get_height())
        bottom_rect = pygame.Rect(self.x, self.bottom_y, self.sprite.get_width(), self.sprite.get_height())
        return top_rect, bottom_rect
