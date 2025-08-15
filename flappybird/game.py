import pygame
import json
from flappybird.bird import Bird
from flappybird.pipe import Pipe
from flappybird.score import Score

class Game:
    """
    Orchestrates the core gameplay loop for Flappy Bird.
    Handles object updates, rendering, collisions, and persistent score tracking.
    """

    def __init__(self, surface, user):
        """
        Set up the game environment and initial state.

        Args:
            surface (pygame.Surface): The display surface where everything will be drawn.
            user (str): Defines control mode ("ai" or "human").
        """
        self.surface = surface
        self.screen_width = surface.get_width()
        self.screen_height = surface.get_height()

        # Core gameplay entities
        self.bird = Bird()
        self.pipes = []
        self.pipe_spawn_timer = 60  # Frames until the next pipe appears

        # Base (ground) visuals and scrolling
        self.base_sprite = pygame.image.load("assets/sprites/base.png").convert_alpha()
        self.base_scroll_speed = 3
        self.base_width = self.base_sprite.get_width()
        self.base_x = 0
        self.base_y = self.screen_height - self.base_sprite.get_height() + 20

        # Background image setup
        self.bg_original = pygame.image.load("assets/sprites/background-day.png").convert()
        self.bg_scaled_height = int(self.screen_height * 1.2)
        self.background = pygame.transform.scale(
            self.bg_original,
            (self.screen_width, self.bg_scaled_height)
        )

        # UI overlays (Game Over and "Get Ready" message)
        self.game_over_sprite = pygame.image.load("assets/sprites/gameover.png").convert_alpha()
        self.get_ready_original = pygame.image.load("assets/sprites/message.png").convert_alpha()
        self.get_ready_width = self.get_ready_original.get_width()
        self.get_ready_height = self.get_ready_original.get_height()
        self.get_ready_sprite = pygame.transform.scale(
            self.get_ready_original,
            (int(self.get_ready_width * 1.4), int(self.get_ready_height * 1.4))
        )

        # Score tracking and persistence
        self.score = Score()
        self.current_score = 0
        self.best_score = self.load_best_score()

        # Game state flags
        self.waiting_to_start = True
        self.game_over = False

        # Sound effects
        self.sfx_die = pygame.mixer.Sound("assets/audio/die.wav")
        self.played_die_sound = False
        self.sfx_jump = pygame.mixer.Sound("assets/audio/wing.wav")
        self.sfx_point = pygame.mixer.Sound("assets/audio/point.wav")

        # Who is playing ("human" or "ai")
        self.user = user


    def update(self):
        """
        Run one frame of game logic and draw the current state.

        Returns:
            tuple:
                reward (float): Feedback signal (useful for AI training).
                done (bool): True if the round has ended.
        """
        self.draw_background()

        # Waiting phase before the game starts
        if self.user == "human" and self.waiting_to_start:
            self.draw_get_ready()
            self.update_base()
            self.draw_base()
            self.bird.jump()  # Small bounce to show the bird is ready
            return 0.0, False

        # When game over screen is active
        if self.game_over:
            self.bird.update()
            self.bird.draw(self.surface)
            self.draw_pipes()
            self.draw_base()
            self.draw_game_over()

            # Update and store best score if necessary
            if self.current_score > self.best_score:
                self.best_score = self.current_score
                self.save_best_score()

            # Play death sound only once
            if not self.played_die_sound:
                self.sfx_die.play()
                self.played_die_sound = True

            # Display score at center
            self.score.draw(
                self.surface,
                self.current_score,
                self.screen_width // 2,
                self.screen_height // 2
            )
            return -1.0, True

        # Ongoing gameplay
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

        # Detect collisions with ground or pipes
        if self.check_collision():
            self.game_over = True
            self.bird.velocity = 0
            return -10, True

        return 0.1, False

    def update_pipes(self):
        """
        Shift pipes to the left, detect when the bird passes them,
        and remove any that have completely left the screen.
        """
        for pipe in self.pipes:
            pipe.update()
            # Bird passes the pipe → increase score
            if not pipe.passed and pipe.x + (pipe.width / 4) < self.bird.x:
                pipe.passed = True
                self.current_score += 1
                self.sfx_point.play()
        # Keep only visible pipes
        self.pipes = [pipe for pipe in self.pipes if pipe.x + pipe.width > 0]

    def draw_pipes(self):
        """Render all pipe objects on the screen."""
        for pipe in self.pipes:
            pipe.draw(self.surface)

    def update_base(self):
        """
        Scroll the ground texture and loop it
        to create continuous movement.
        """
        self.base_x -= self.base_scroll_speed
        if self.base_x <= -self.base_width:
            self.base_x = 0

    def draw_base(self):
        """Tile the ground image horizontally to fill the width."""
        self.surface.blit(self.base_sprite, (self.base_x, self.base_y))
        self.surface.blit(self.base_sprite, (self.base_x + self.base_width, self.base_y))
        self.surface.blit(self.base_sprite, (self.base_x + self.base_width * 2, self.base_y))

    def draw_background(self):
        """Draw the background image with a fixed vertical shift."""
        self.surface.blit(self.background, (0, -60))

    def draw_game_over(self):
        """Center and draw the 'Game Over' banner."""
        x = (self.screen_width - self.game_over_sprite.get_width()) // 2
        y = self.screen_height // 4
        self.surface.blit(self.game_over_sprite, (x, y))

    def check_collision(self):
        """
        Detect whether the bird has hit the ground, the ceiling, or a pipe.

        Returns:
            bool: True if a collision is detected.
        """
        bird_rect = self.bird.get_rect()

        # Ground collision
        if bird_rect.bottom >= self.base_y:
            self.bird.velocity = -0.6
            return True
        # Ceiling collision
        if bird_rect.top <= 0:
            return True

        # Pipe collision
        for pipe in self.pipes:
            top_rect, bottom_rect = pipe.get_rects()
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                return True
        return False

    def draw_get_ready(self):
        """Position and render the 'Get Ready' message."""
        x = (self.screen_width - self.get_ready_sprite.get_width()) // 2
        y = self.screen_height // 8
        self.surface.blit(self.get_ready_sprite, (x, y))

    def reset(self):
        """
        Reinitialize all variables and objects to start a new round.
        """
        self.bird.reset()
        self.pipes.clear()
        self.current_score = 0
        self.waiting_to_start = False
        self.game_over = False
        self.played_die_sound = False

    def load_best_score(self):
        """
        Retrieve the highest recorded score from disk.

        Returns:
            int: The saved best score, or 0 if no file is found.
        """
        try:
            with open("flappybird/score.json", "r") as f:
                data = json.load(f)
                return data.get("best_score", 0)
        except:
            return 0

    def save_best_score(self):
        """Store the current best score to disk."""
        with open("flappybird/score.json", "w") as f:
            json.dump({"best_score": self.best_score}, f)

    def spawn_pipe(self):
        """Add a new pipe object starting at the right edge."""
        self.pipes.append(Pipe(x=self.screen_width))
