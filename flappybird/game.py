import pygame
import json
from flappybird.bird import Bird
from flappybird.pipe import Pipe
from flappybird.score import Score

class Game:
    """
    Main game class handling the Flappy Bird gameplay mechanics,
    rendering, and game state management.
    """

    def __init__(self, surface, user):
        """
        Initialize the game with the display surface.

        Loads necessary assets, initializes the bird, pipes, score,
        and game state flags.

        Args:
            surface (pygame.Surface): The main display surface for rendering.
        """
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
        self.best_score = self.load_best_score()

        self.waiting_to_start = True
        self.game_over = False

        self.sfx_die = pygame.mixer.Sound("assets/audio/die.wav")
        self.played_die_sound = False
        self.sfx_jump = pygame.mixer.Sound("assets/audio/wing.wav")
        self.sfx_point = pygame.mixer.Sound("assets/audio/point.wav")

        self.user = user

    def load_best_score(self):
        """
        Load the best score from a JSON file.

        Returns:
            int: The best recorded score or 0 if file is missing or corrupted.
        """
        try:
            with open("flappybird/score.json", "r") as f:
                data = json.load(f)
                return data.get("best_score", 0)
        except:
            return 0

    def save_best_score(self):
        """
        Save the current best score to a JSON file.
        """
        with open("flappybird/score.json", "w") as f:
            json.dump({"best_score": self.best_score}, f)

    def spawn_pipe(self):
        """
        Create and append a new Pipe object at the right edge of the screen.
        """
        self.pipes.append(Pipe(x=self.screen_width))

    def update(self):
        """
        Update the game state and render the current frame.

        Handles game phases including waiting to start, gameplay, and game over.
        Manages pipe spawning, bird and pipe updates, collision detection,
        and score updates.
        """
        self.draw_background()
        if self.user == "human":
            if self.waiting_to_start:
                self.bird.jump()
                self.draw_get_ready()
                self.bird.draw(self.surface)
                self.update_base()
                self.draw_base()
                return

        if self.game_over:
            self.check_collision()
            self.bird.update()
            self.bird.draw(self.surface)
            self.draw_pipes()
            self.draw_base()
            self.draw_game_over()
            if self.current_score > self.best_score:
                self.best_score = self.current_score
                self.save_best_score()
            if not self.played_die_sound:
                self.sfx_die.play()
                self.played_die_sound = True
            self.score.draw(self.surface, self.current_score, self.screen_width // 2, self.screen_height // 2)
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
        """
        Update positions of all pipes, check for passing events to increase score,
        and remove pipes that have moved off-screen.
        """
        for pipe in self.pipes:
            pipe.update()
            if not pipe.passed and pipe.x + (pipe.width / 4) < self.bird.x:
                pipe.passed = True
                self.current_score += 1
                self.sfx_point.play()
        self.pipes = [pipe for pipe in self.pipes if pipe.x + pipe.width > 0]

    def draw_pipes(self):
        """
        Draw all pipes on the current surface.
        """
        for pipe in self.pipes:
            pipe.draw(self.surface)

    def update_base(self):
        """
        Update the horizontal scrolling position of the base (ground).
        """
        self.base_x -= self.base_scroll_speed
        if self.base_x <= -self.base_width:
            self.base_x = 0

    def draw_base(self):
        """
        Render the base sprite multiple times to fill the width of the screen.
        """
        self.surface.blit(self.base_sprite, (self.base_x, self.base_y))
        self.surface.blit(self.base_sprite, (self.base_x + self.base_width, self.base_y))
        self.surface.blit(self.base_sprite, (self.base_x + self.base_width * 2, self.base_y))

    def draw_background(self):
        """
        Render the background image onto the surface, slightly offset vertically.
        """
        self.surface.blit(self.background, (0, -60))

    def draw_game_over(self):
        """
        Draw the game over sprite centered horizontally near the top quarter of the screen.
        """
        x = (self.screen_width - self.game_over_sprite.get_width()) // 2
        y = (self.screen_height - self.game_over_sprite.get_height()) // 4
        self.surface.blit(self.game_over_sprite, (x, y))

    def check_collision(self):
        """
        Check if the bird collides with the base or any pipes.

        Returns:
            bool: True if collision detected, False otherwise.
        """
        bird_rect = self.bird.get_rect()
        if bird_rect.bottom >= self.base_y:
            self.bird.velocity = -0.6
            return True
        for pipe in self.pipes:
            top_rect, bottom_rect = pipe.get_rects()
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                return True
        return False

    def draw_get_ready(self):
        """
        Draw the "Get Ready" message sprite centered horizontally
        near the top eighth of the screen.
        """
        x = (self.screen_width - self.get_ready_sprite.get_width()) // 2
        y = self.screen_height // 8
        self.surface.blit(self.get_ready_sprite, (x, y))

    def reset(self):
        """
        Reset the game state to start a new game.

        Resets the bird, pipes, score, and game state flags.
        """
        self.bird.reset()
        self.pipes.clear()
        self.current_score = 0
        self.game_over = False
        self.played_die_sound = False
