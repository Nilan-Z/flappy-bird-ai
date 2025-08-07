import pygame
from flappybird.bird import Bird
from flappybird.pipe import Pipe
from flappybird.score import Score

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.screen_width = surface.get_width()
        self.screen_height = surface.get_height()

        self.bird = Bird()
        self.pipes = []
        self.pipe_spawn_timer = 60

        self.base_sprite = pygame.image.load("assets/sprites/base.png").convert_alpha()
        self.base_scroll_speed = 3
        self.base_width = self.base_sprite.get_width()
        self.base_x = 0
        self.base_y = self.screen_height - self.base_sprite.get_height() + 20

        self.bg_original = pygame.image.load("assets/sprites/background-day.png").convert()
        self.bg_scaled_height = int(self.screen_height * 1.2)
        self.background = pygame.transform.scale(self.bg_original, (self.screen_width, self.bg_scaled_height))

        self.game_over_sprite = pygame.image.load("assets/sprites/gameover.png").convert_alpha()

        self.get_ready_original = pygame.image.load("assets/sprites/message.png").convert_alpha()
        self.get_ready_width = self.get_ready_original.get_width()
        self.get_ready_height = self.get_ready_original.get_height()
        self.get_ready_sprite = pygame.transform.scale(
            self.get_ready_original,
            (int(self.get_ready_width * 1.4), int(self.get_ready_height * 1.4))
        )

        self.score = Score()
        self.current_score = 0

        self.waiting_to_start = True
        self.game_over = False

    def spawn_pipe(self):
        self.pipes.append(Pipe(x=self.screen_width))

    def update(self):
        self.draw_background()

        if self.waiting_to_start:
            self.bird.gravity = 0
            self.bird.draw(self.surface)
            self.update_base()
            self.draw_base()
            self.draw_get_ready()
            return

        if self.game_over:
            self.bird.draw(self.surface)
            self.draw_pipes()
            self.draw_base()
            self.draw_game_over()
            return

        self.pipe_spawn_timer += 1
        if self.pipe_spawn_timer >= 80:
            self.spawn_pipe()
            self.pipe_spawn_timer = 0

        self.bird.draw(self.surface)
        self.update_pipes()
        self.draw_pipes()
        self.update_base()
        self.draw_base()
        self.score.draw(self.surface, self.current_score, self.screen_width // 2, 30)

        if self.check_collision():
            self.game_over = True
            self.bird.velocity = 0

    def update_pipes(self):
        for pipe in self.pipes:
            pipe.update()
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.current_score += 1
        self.pipes = [pipe for pipe in self.pipes if pipe.x + pipe.width > 0]

    def draw_pipes(self):
        for pipe in self.pipes:
            pipe.draw(self.surface)

    def update_base(self):
        self.base_x -= self.base_scroll_speed
        if self.base_x <= -self.base_width:
            self.base_x = 0

    def draw_base(self):
        self.surface.blit(self.base_sprite, (self.base_x, self.base_y))
        self.surface.blit(self.base_sprite, (self.base_x + self.base_width, self.base_y))
        self.surface.blit(self.base_sprite, (self.base_x + self.base_width * 2, self.base_y))

    def draw_background(self):
        self.surface.blit(self.background, (0, -60))

    def draw_game_over(self):
        x = (self.screen_width - self.game_over_sprite.get_width()) // 2
        y = (self.screen_height - self.game_over_sprite.get_height()) // 4
        self.surface.blit(self.game_over_sprite, (x, y))

    def check_collision(self):
        bird_rect = self.bird.get_rect()
        if bird_rect.bottom >= self.base_y:
            return True
        for pipe in self.pipes:
            top_rect, bottom_rect = pipe.get_rects()
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                return True
        return False

    def draw_get_ready(self):
        x = (self.screen_width - self.get_ready_sprite.get_width()) // 2
        y = self.screen_height // 8
        self.surface.blit(self.get_ready_sprite, (x, y))
