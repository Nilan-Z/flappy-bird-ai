import pygame
import random
from typing import Tuple

from flappybird.path_utils import load_yaml_config, resolve_project_path


class Pipe:
    def __init__(self, x: int):
        # Load configuration
        cfg = load_yaml_config()

        # Load and scale pipe sprite
        self.original_sprite: pygame.Surface = pygame.image.load(
            str(resolve_project_path("assets/sprites/pipe-green.png"))
        ).convert_alpha()
        self.sprite: pygame.Surface = pygame.transform.scale(
            self.original_sprite,
            (int(self.original_sprite.get_width() * 1.5), self.original_sprite.get_height())
        )
        self.flipped_sprite: pygame.Surface = pygame.transform.flip(self.sprite, False, True)

        self.gap: int = int(cfg.get("pipe_gap", 100))
        self.velocity: int = 3
        self.x: int = x
        self.passed: bool = False
        self.width: int = self.sprite.get_width()

        self.set_height()

    def set_height(self) -> None:
        height = random.randint(50, 300)
        self.top_y: int = height - self.sprite.get_height()
        self.bottom_y: int = height + self.gap

    def update(self) -> None:
        self.x -= self.velocity

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.flipped_sprite, (self.x, self.top_y))
        surface.blit(self.sprite, (self.x, self.bottom_y))

    def get_rects(self) -> Tuple[pygame.Rect, pygame.Rect]:
        top_rect = pygame.Rect(self.x, self.top_y, self.sprite.get_width(), self.sprite.get_height())
        bottom_rect = pygame.Rect(self.x, self.bottom_y, self.sprite.get_width(), self.sprite.get_height())
        return top_rect, bottom_rect
