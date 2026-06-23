import pygame
import random
from typing import List

from flappybird.path_utils import resolve_project_path

class Bird:
    def __init__(self, mode: str):
        self.mode: str = mode

        # Select bird color randomly
        self.sprites_color: str = random.choice(["red", "blue", "yellow"])

        # Load base sprites
        sprite_paths = {
            "red": ["assets/sprites/redbird-upflap.png",
                    "assets/sprites/redbird-midflap.png",
                    "assets/sprites/redbird-downflap.png"],
            "blue": ["assets/sprites/bluebird-upflap.png",
                     "assets/sprites/bluebird-midflap.png",
                     "assets/sprites/bluebird-downflap.png"],
            "yellow": ["assets/sprites/yellowbird-upflap.png",
                       "assets/sprites/yellowbird-midflap.png",
                       "assets/sprites/yellowbird-downflap.png"]
        }

        # Load and convert sprites
        base_sprites: List[pygame.Surface] = []
        for path in sprite_paths[self.sprites_color]:
            resolved_path = resolve_project_path(path)
            img = pygame.image.load(str(resolved_path))
            img = img.convert_alpha() if mode == "human" else img.convert()
            base_sprites.append(img)

        # Scale sprites
        self.sprites: List[pygame.Surface] = [
            pygame.transform.scale(sprite, (int(sprite.get_width()*1.5), int(sprite.get_height()*1.5)))
            for sprite in base_sprites
        ]

        # Animation control
        self.current_sprite_index: int = 0
        self.animation_frame: int = 0

        # Position
        self.x: int = 100
        self.y: float = 235

        # Physics
        self.normal_gravity: float = 0.2
        self.heavy_gravity: float = 0.3
        self.gravity: float = self.normal_gravity
        self.jump_force: float = -5.5
        self.velocity: float = 0

        # Rotation
        self.angle: float = 0
        self.max_fall_speed: float = 14
        self.rotation_speed: float = 10
        self.fall_rotation_threshold: float = 5

    def jump(self) -> None:
        """Make the bird jump upwards."""
        self.velocity = self.jump_force
        self.angle = 25
        self.gravity = self.normal_gravity

    def update(self) -> None:
        """Update bird position, velocity and rotation."""
        if self.velocity > 0:
            self.gravity = self.heavy_gravity

        self.velocity += self.gravity
        self.velocity = min(self.velocity, self.max_fall_speed)
        self.y += self.velocity

        if self.velocity < 0:
            self.angle = min(self.angle + self.rotation_speed, 25)
        elif self.velocity > self.fall_rotation_threshold:
            self.angle = max(self.angle - self.rotation_speed*1.5, -85)

    def draw(self, surface: pygame.Surface) -> pygame.Rect:
        """Draw bird on the screen and return its rect."""
        self.animation_frame += 1
        if self.animation_frame == 6:
            self.animation_frame = 0
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites)

        sprite = self.sprites[self.current_sprite_index]
        rotated_sprite = pygame.transform.rotate(sprite, self.angle)
        rect = rotated_sprite.get_rect(center=(self.x + sprite.get_width()//2,
                                               self.y + sprite.get_height()//2))
        surface.blit(rotated_sprite, rect.topleft)
        return rect

    def get_rect(self) -> pygame.Rect:
        """Return hitbox of the bird."""
        sprite = self.sprites[self.current_sprite_index]
        return pygame.Rect(self.x, self.y, sprite.get_width() - 10, sprite.get_height() - 10)

    def reset(self) -> None:
        """Reset bird to initial state."""
        self.current_sprite_index = 0
        self.animation_frame = 0
        self.x = 100
        self.y = 235
        self.gravity = self.normal_gravity
        self.velocity = 0
        self.angle = 0
