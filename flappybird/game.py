import pygame
from flappybird.bird import Bird
from flappybird.pipe import Pipe

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.bird = Bird()
        self.pipes = []
        self.spawn_timer = 0

        self.base = pygame.image.load("assets/sprites/base.png").convert_alpha()
        self.base_scroll_speed = 3
        self.base_width = self.base.get_width()
        self.base_x = 0

        self.background = pygame.image.load("assets/sprites/background-day.png").convert()
        self.screen_width = surface.get_width()
        self.screen_height = surface.get_height()

        self.game_over_sprite = pygame.image.load("assets/sprites/gameover.png").convert_alpha()
        self.game_over = False

    def spawn_pipe(self):
        self.pipes.append(Pipe(x=self.screen_width))

    def update(self):
        self.draw_background()

        if self.game_over:
            self.draw_game_over()
            return

        self.bird.draw(self.surface)

        self.spawn_timer += 1
        if self.spawn_timer >= 90:
            self.spawn_pipe()
            self.spawn_timer = 0

        for pipe in self.pipes:
            pipe.update()
            pipe.draw(self.surface)

        self.pipes = [pipe for pipe in self.pipes if pipe.x + pipe.pipe_image.get_width() > 0]

        self.base_x -= self.base_scroll_speed
        if self.base_x <= -self.base_width:
            self.base_x = 0

        base_y = self.screen_height - self.base.get_height() / 1.7
        self.surface.blit(self.base, (self.base_x, base_y))
        self.surface.blit(self.base, (self.base_x + self.base_width, base_y))

        if self.check_collision():
            self.game_over = True
            self.bird.velocity = 0

    def draw_background(self):
        self.surface.blit(self.background, (0, 0))

    def draw_game_over(self):
        x = (self.screen_width - self.game_over_sprite.get_width()) // 2
        y = (self.screen_height - self.game_over_sprite.get_height()) // 2
        self.surface.blit(self.game_over_sprite, (x, y))

    def check_collision(self):
        bird_rect = self.bird.get_rect()
        base_y = self.screen_height - self.base.get_height() / 1.7

        if bird_rect.bottom >= base_y:
            return True

        for pipe in self.pipes:
            top_rect, bottom_rect = pipe.get_rects()
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                return True

        return False
