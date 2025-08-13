import pygame
import json
from flappybird.bird import Bird
from flappybird.pipe import Pipe
from flappybird.score import Score

class Game:
    """
    Main Flappy Bird game logic handler.
    Manages bird physics, pipe spawning, score tracking, rendering, and collision detection.
    """

    def __init__(self, surface, user):
        """
        Initialize the game with required assets and default state.

        Args:
            surface (pygame.Surface): Main display surface for rendering.
            user (str): "ai" for AI-controlled gameplay, "human" for manual control.
        """
        self.surface = surface
        self.screen_width = surface.get_width()
        self.screen_height = surface.get_height()

        # Game objects
        self.bird = Bird()
        self.pipes = []
        self.pipe_spawn_timer = 60

        # Base (ground) sprite setup
        self.base_sprite = pygame.image.load("assets/sprites/base.png").convert_alpha()
        self.base_scroll_speed = 3
        self.base_width = self.base_sprite.get_width()
        self.base_x = 0
        self.base_y = self.screen_height - self.base_sprite.get_height() + 20

        # Background setup
        self.bg_original = pygame.image.load("assets/sprites/background-day.png").convert()
        self.bg_scaled_height = int(self.screen_height * 1.2)
        self.background = pygame.transform.scale(
            self.bg_original,
            (self.screen_width, self.bg_scaled_height)
        )

        # UI assets
        self.game_over_sprite = pygame.image.load("assets/sprites/gameover.png").convert_alpha()
        self.get_ready_original = pygame.image.load("assets/sprites/message.png").convert_alpha()
        self.get_ready_width = self.get_ready_original.get_width()
        self.get_ready_height = self.get_ready_original.get_height()
        self.get_ready_sprite = pygame.transform.scale(
            self.get_ready_original,
            (int(self.get_ready_width * 1.4), int(self.get_ready_height * 1.4))
        )

        # Score system
        self.score = Score()
        self.current_score = 0
        self.best_score = self.load_best_score()

        # Game state flags
        self.waiting_to_start = True
        self.game_over = False

        # Audio
        self.sfx_die = pygame.mixer.Sound("assets/audio/die.wav")
        self.played_die_sound = False
        self.sfx_jump = pygame.mixer.Sound("assets/audio/wing.wav")
        self.sfx_point = pygame.mixer.Sound("assets/audio/point.wav")

        self.user = user

    def load_best_score(self):
        """
        Load the best score from a JSON file.

        Returns:
            int: Best recorded score, or 0 if file not found or invalid.
        """
        try:
            with open("flappybird/score.json", "r") as f:
                data = json.load(f)
                return data.get("best_score", 0)
        except:
            return 0

    def save_best_score(self):
        """
        Save the best score to a JSON file.
        """
        with open("flappybird/score.json", "w") as f:
            json.dump({"best_score": self.best_score}, f)

    def spawn_pipe(self):
        """
        Spawn a new pipe at the right edge of the screen.
        """
        self.pipes.append(Pipe(x=self.screen_width))

    def update_logic(self):
        """
        Update game state and handle rendering.

        Returns:
            tuple:
                - reward (float): Reward signal for AI training.
                - done (bool): True if the game has ended.
        """
        self.draw_background()

        # Initial "Get Ready" phase for human players
        if self.user == "human" and self.waiting_to_start:
            self.draw_get_ready()
            self.bird.draw(self.surface)
            self.update_base()
            self.draw_base()
            return 0.0, False

        # Game Over phase
        if self.game_over:
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

            self.score.draw(
                self.surface,
                self.current_score,
                self.screen_width // 2,
                self.screen_height // 2
            )
            return -1.0, True

        # Main game phase
        self.pipe_spawn_timer += 1
        if self.pipe_spawn_timer >= 80:
            self.spawn_pipe()
            self.pipe_spawn_timer = 0

        self.bird.update()
        self.bird.draw(self.surface)

        self.update_pipes()
        self.draw_pipes()
        self.update_base()
        self.draw_base()

        self.score.draw(self.surface, self.current_score, self.screen_width // 2, 30)

        # Collision detection
        if self.check_collision():
            self.game_over = True
            self.bird.velocity = 0
            return -1.0, True

        return 0.1, False

    def update_pipes(self):
        """
        Move pipes leftward, update score when passing,
        and remove pipes that are off-screen.
        """
        for pipe in self.pipes:
            pipe.update()
            if not pipe.passed and pipe.x + (pipe.width / 4) < self.bird.x:
                pipe.passed = True
                self.current_score += 1
                self.sfx_point.play()
        self.pipes = [pipe for pipe in self.pipes if pipe.x + pipe.width > 0]

    def draw_pipes(self):
        """Draw all active pipes."""
        for pipe in self.pipes:
            pipe.draw(self.surface)

    def update_base(self):
        """Scroll the base (ground) to create movement illusion."""
        self.base_x -= self.base_scroll_speed
        if self.base_x <= -self.base_width:
            self.base_x = 0

    def draw_base(self):
        """Draw the base repeatedly to fill the width."""
        self.surface.blit(self.base_sprite, (self.base_x, self.base_y))
        self.surface.blit(self.base_sprite, (self.base_x + self.base_width, self.base_y))
        self.surface.blit(self.base_sprite, (self.base_x + self.base_width * 2, self.base_y))

    def draw_background(self):
        """Draw the background image with a vertical offset."""
        self.surface.blit(self.background, (0, -60))

    def draw_game_over(self):
        """Draw the Game Over image centered near the top."""
        x = (self.screen_width - self.game_over_sprite.get_width()) // 2
        y = self.screen_height // 4
        self.surface.blit(self.game_over_sprite, (x, y))

    def check_collision(self):
        """
        Check collision between bird and ground or pipes.

        Returns:
            bool: True if collision occurs, else False.
        """
        bird_rect = self.bird.get_rect()

        # Collision with ground
        if bird_rect.bottom >= self.base_y:
            self.bird.velocity = -0.6
            return True
        # Collision with top of the screen
        if bird_rect.top <= 0:
            return True

        # Collision with pipes
        for pipe in self.pipes:
            top_rect, bottom_rect = pipe.get_rects()
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                return True
        return False

    def draw_get_ready(self):
        """Draw the 'Get Ready' prompt centered near the top."""
        x = (self.screen_width - self.get_ready_sprite.get_width()) // 2
        y = self.screen_height // 8
        self.surface.blit(self.get_ready_sprite, (x, y))

    def reset(self):
        """
        Reset all game objects and state for a new game.
        """
        self.bird.reset()
        self.pipes.clear()
        self.current_score = 0
        self.waiting_to_start = False
        self.game_over = False
        self.played_die_sound = False
