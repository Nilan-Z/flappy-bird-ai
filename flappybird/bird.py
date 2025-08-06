import pygame

class Bird():
    def __init__(self):
        # Initialize bird properties
        self.sprites = [      
            pygame.image.load("assets/sprites/redbird-upflap.png").convert_alpha(),
            pygame.image.load("assets/sprites/redbird-midflap.png").convert_alpha(),
            pygame.image.load("assets/sprites/redbird-downflap.png").convert_alpha()
        ]
        self.current_sprite = 0  # index du sprite courant pour l’animation
        self.x = 50
        self.y = 250
        self.gravity = 0.5
        self.jump_strength = -10
        self.velocity = 0
        self.frame = 0

    def draw(self, surface):
        self.frame += 1
        surface.blit(self.sprites[self.current_sprite], (self.x, self.y))
        if self.frame == 6:
            self.frame = 0
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.sprites[self.current_sprite].get_width(), self.sprites[self.current_sprite].get_height())
