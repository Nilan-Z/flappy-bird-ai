import pygame

class Bird:
    def __init__(self):
        base_sprites = [
            pygame.image.load("assets/sprites/redbird-upflap.png").convert_alpha(),
            pygame.image.load("assets/sprites/redbird-midflap.png").convert_alpha(),
            pygame.image.load("assets/sprites/redbird-downflap.png").convert_alpha()
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
        self.velocity = self.jump_force
        self.angle = 25
        self.gravity = self.normal_gravity  

    def update(self):

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
        sprite = self.sprites[self.current_sprite_index]
        return pygame.Rect(self.x, self.y, sprite.get_width(), sprite.get_height())
