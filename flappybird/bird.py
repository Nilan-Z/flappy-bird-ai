import pygame
import random

class Bird:
    def __init__(self, mode):
        self.mode = mode

        # Select bird color randomly
        self.sprites_color = random.choice(["red", "blue", "yellow"])

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
        base_sprites = []
        for path in sprite_paths[self.sprites_color]:
            img = pygame.image.load(path)
            img = img.convert_alpha() if mode == "human" else img.convert()
            base_sprites.append(img)

        # Scale sprites
        self.sprites = [pygame.transform.scale(sprite, (int(sprite.get_width()*1.5), int(sprite.get_height()*1.5)))
                        for sprite in base_sprites]

        # Animation control
        self.current_sprite_index = 0
        self.animation_frame = 0

        # Position
        self.x = 100
        self.y = 235

        # Physics
        self.normal_gravity = 0.2
        self.heavy_gravity = 0.3
        self.gravity = self.normal_gravity
        self.jump_force = -5.5
        self.velocity = 0

        # Rotation
        self.angle = 0
        self.max_fall_speed = 14
        self.rotation_speed = 10
        self.fall_rotation_threshold = 5

    def jump(self):
        # Apply jump
        self.velocity = self.jump_force
        self.angle = 25
        self.gravity = self.normal_gravity

    def update(self):
        # Gravity adjustment
        if self.velocity > 0:
            self.gravity = self.heavy_gravity

        # Update velocity
        self.velocity += self.gravity
        self.velocity = min(self.velocity, self.max_fall_speed)

        # Move vertically
        self.y += self.velocity

        # Rotation adjustment
        if self.velocity < 0:
            self.angle = min(self.angle + self.rotation_speed, 25)
        elif self.velocity > self.fall_rotation_threshold:
            self.angle = max(self.angle - self.rotation_speed*1.5, -85)

    def draw(self, surface):
        # Animate sprite
        self.animation_frame += 1
        if self.animation_frame == 6:
            self.animation_frame = 0
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites)

        # Rotate and render sprite
        sprite = self.sprites[self.current_sprite_index]
        rotated_sprite = pygame.transform.rotate(sprite, self.angle)
        rect = rotated_sprite.get_rect(center=(self.x + sprite.get_width()//2,
                                               self.y + sprite.get_height()//2))
        surface.blit(rotated_sprite, rect.topleft)

    def get_rect(self):
        # Return hitbox
        sprite = self.sprites[self.current_sprite_index]
        return pygame.Rect(self.x, self.y, sprite.get_width() - 10, sprite.get_height() - 10)

    def reset(self):
        # Reset animation
        self.current_sprite_index = 0
        self.animation_frame = 0

        # Reset position and physics
        self.x = 100
        self.y = 235
        self.gravity = self.normal_gravity
        self.velocity = 0
        self.angle = 0
