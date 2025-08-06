import pygame

class Bird:
    def __init__(self):
        original_sprites = [
            pygame.image.load("assets/sprites/redbird-upflap.png").convert_alpha(),
            pygame.image.load("assets/sprites/redbird-midflap.png").convert_alpha(),
            pygame.image.load("assets/sprites/redbird-downflap.png").convert_alpha()
        ]
        
        self.sprites = []
        for sprite in original_sprites:
            width = sprite.get_width()
            height = sprite.get_height()
            scaled_sprite = pygame.transform.scale(sprite, (int(width * 1.2), int(height * 1.2)))
            self.sprites.append(scaled_sprite)

        self.current_sprite = 0
        self.x = 50
        self.y = 250
        self.gravity = 8
        self.jump_strength = -5
        self.velocity = 0
        self.frame = 0
        self.angle = 0
        self.max_fall_speed = 50
        self.rotation_speed = 4

    def jump(self):
        self.velocity = self.jump_strength
        self.angle = 25

    def update(self):
        self.velocity += self.gravity
        if self.velocity > self.max_fall_speed:
            self.velocity = self.max_fall_speed

        self.y += self.velocity

        if self.velocity < 0:
            self.angle = min(self.angle + self.rotation_speed, 25)
        else:
            self.angle = max(self.angle - self.rotation_speed, -85)

    def draw(self, surface):
        self.frame += 1
        if self.frame == 6:
            self.frame = 0
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)

        rotated_image = pygame.transform.rotate(self.sprites[self.current_sprite], self.angle)
        rect = rotated_image.get_rect(center=(self.x + self.sprites[self.current_sprite].get_width() // 2,
                                              self.y + self.sprites[self.current_sprite].get_height() // 2))
        surface.blit(rotated_image, rect.topleft)

    def get_rect(self):
        return pygame.Rect(self.x, self.y,
                           self.sprites[self.current_sprite].get_width(),
                           self.sprites[self.current_sprite].get_height())
