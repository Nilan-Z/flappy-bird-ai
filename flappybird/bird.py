import pygame
import random

class Bird:
    def __init__(self):
        """
        Initialize a Bird object with randomized color sprites and default physical properties.

        Attributes:
            sprites_color (str): The color of the bird sprite, randomly chosen from ["red", "blue", "yellow"].
            sprites (list): List of scaled pygame.Surface objects representing animation frames.
            current_sprite_index (int): Index of the current sprite used for animation.
            animation_frame (int): Counter to control animation frame switching.
            x (int): Horizontal position of the bird on the screen.
            y (int): Vertical position of the bird on the screen.
            normal_gravity (float): Standard gravity applied when bird is rising.
            heavy_gravity (float): Increased gravity applied when bird is falling.
            gravity (float): Current gravity applied to the bird.
            jump_force (int): Initial velocity applied when the bird jumps.
            velocity (float): Current vertical velocity of the bird.
            angle (float): Current rotation angle of the bird sprite.
            max_fall_speed (int): Maximum velocity when falling.
            rotation_speed (int): Speed at which the bird rotates during movement.
            fall_rotation_threshold (int): Velocity threshold after which bird rotates downwards sharply.
        """
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

        self.sprites = []
        for sprite in base_sprites:
            width = sprite.get_width()
            height = sprite.get_height()
            scaled_sprite = pygame.transform.scale(sprite, (int(width * 1.5), int(height * 1.5)))
            self.sprites.append(scaled_sprite)

        self.current_sprite_index = 0
        self.animation_frame = 0

        self.x = 100
        self.y = 235

        self.normal_gravity = 0.5           
        self.heavy_gravity = 0.6           
        self.gravity = self.normal_gravity  
        self.jump_force = -8
        self.velocity = 0

        self.angle = 0
        self.max_fall_speed = 14
        self.rotation_speed = 10
        self.fall_rotation_threshold = 5

    def jump(self):
        """
        Makes the bird jump by setting the velocity to jump_force, adjusting the angle,
        and setting gravity to normal gravity for ascent.
        """
        self.velocity = self.jump_force
        self.angle = 25
        self.gravity = self.normal_gravity  

    def update(self):
        """
        Updates the bird's position, velocity, gravity, and rotation angle based on current movement.

        Applies heavier gravity when falling, caps the fall speed, updates vertical position,
        and adjusts the sprite rotation angle to simulate natural bird movement.
        """
        if self.velocity > 0:
            self.gravity = self.heavy_gravity

        self.velocity += self.gravity
        if self.velocity > self.max_fall_speed:
            self.velocity = self.max_fall_speed

        self.y += self.velocity

        if self.velocity < 0:
            self.angle = min(self.angle + self.rotation_speed, 25)
        elif self.velocity > self.fall_rotation_threshold:
            self.angle = max(self.angle - self.rotation_speed * 1.5, -85)

    def draw(self, surface):
        """
        Draws the bird sprite onto the given surface with the current animation frame and rotation.

        Args:
            surface (pygame.Surface): The surface on which to draw the bird.
        """
        self.animation_frame += 1
        if self.animation_frame == 6:
            self.animation_frame = 0
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites)

        sprite = self.sprites[self.current_sprite_index]
        rotated_sprite = pygame.transform.rotate(sprite, self.angle)
        rect = rotated_sprite.get_rect(center=(self.x + sprite.get_width() // 2,
                                               self.y + sprite.get_height() // 2))
        surface.blit(rotated_sprite, rect.topleft)

    def get_rect(self):
        """
        Returns the pygame.Rect representing the bird's current position and size, 
        useful for collision detection.

        Returns:
            pygame.Rect: Rectangle bounding the bird's current sprite at its position.
        """
        sprite = self.sprites[self.current_sprite_index]
        return pygame.Rect(self.x, self.y, sprite.get_width(), sprite.get_height())
    
    def reset(self):
        """
        Resets the bird's position, velocity, angle, and animation state to initial values.
        """
        self.x = 100
        self.y = 235
        self.velocity = 0
        self.angle = 0
        self.current_sprite_index = 0
        self.animation_frame = 0
        self.gravity = self.normal_gravity
