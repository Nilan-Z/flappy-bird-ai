import pygame
import random

class Bird:
    def __init__(self):
        # Load default red bird sprites
        base_sprites = [
            pygame.image.load("assets/sprites/redbird-upflap.png").convert_alpha(),
            pygame.image.load("assets/sprites/redbird-midflap.png").convert_alpha(),
            pygame.image.load("assets/sprites/redbird-downflap.png").convert_alpha()
        ]

        # Randomly select bird color and load corresponding sprites
        self.sprites_color = random.choice(["red", "blue", "yellow"])
        if self.sprites_color == "red":
            base_sprites = [
                pygame.image.load("assets/sprites/redbird-upflap.png").convert_alpha(),
                pygame.image.load("assets/sprites/redbird-midflap.png").convert_alpha(),
                pygame.image.load("assets/sprites/redbird-downflap.png").convert_alpha()
            ]
        elif self.sprites_color == "blue":
            base_sprites = [
                pygame.image.load("assets/sprites/bluebird-upflap.png").convert_alpha(),
                pygame.image.load("assets/sprites/bluebird-midflap.png").convert_alpha(),
                pygame.image.load("assets/sprites/bluebird-downflap.png").convert_alpha()
            ]
        else:
            base_sprites = [
                pygame.image.load("assets/sprites/yellowbird-upflap.png").convert_alpha(),
                pygame.image.load("assets/sprites/yellowbird-midflap.png").convert_alpha(),
                pygame.image.load("assets/sprites/yellowbird-downflap.png").convert_alpha()
            ]

        # Scale sprites by 1.5x
        self.sprites = []
        for sprite in base_sprites:
            width = sprite.get_width()
            height = sprite.get_height()
            scaled_sprite = pygame.transform.scale(sprite, (int(width * 1.5), int(height * 1.5)))
            self.sprites.append(scaled_sprite)

        # Animation control
        self.current_sprite_index = 0
        self.animation_frame = 0

        # Initial position
        self.x = 100
        self.y = 235

        # Physics settings
        self.normal_gravity = 0.2
        self.heavy_gravity = 0.3
        self.gravity = self.normal_gravity
        self.jump_force = -5.5
        self.velocity = 0

        # Rotation behavior
        self.angle = 0
        self.max_fall_speed = 14
        self.rotation_speed = 10
        self.fall_rotation_threshold = 5

    def jump(self):
        # Apply jump impulse
        self.velocity = self.jump_force
        self.angle = 25
        self.gravity = self.normal_gravity

    def update(self):
        # Switch to heavier gravity when falling
        if self.velocity > 0:
            self.gravity = self.heavy_gravity

        # Update velocity and clamp max fall speed
        self.velocity += self.gravity
        if self.velocity > self.max_fall_speed:
            self.velocity = self.max_fall_speed

        # Apply vertical movement
        self.y += self.velocity

        # Adjust rotation based on movement
        if self.velocity < 0:
            self.angle = min(self.angle + self.rotation_speed, 25)
        elif self.velocity > self.fall_rotation_threshold:
            self.angle = max(self.angle - self.rotation_speed * 1.5, -85)

    def draw(self, surface):
        # Cycle sprite every 6 frames
        self.animation_frame += 1
        if self.animation_frame == 6:
            self.animation_frame = 0
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites)

        # Rotate and draw sprite
        sprite = self.sprites[self.current_sprite_index]
        rotated_sprite = pygame.transform.rotate(sprite, self.angle)
        rect = rotated_sprite.get_rect(center=(self.x + sprite.get_width() // 2,
                                               self.y + sprite.get_height() // 2))
        surface.blit(rotated_sprite, rect.topleft)

    def get_rect(self):
        # Return hitbox of current sprite
        sprite = self.sprites[self.current_sprite_index]
        return pygame.Rect(self.x, self.y, sprite.get_width(), sprite.get_height())
