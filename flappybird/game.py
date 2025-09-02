import pygame
import json
from flappybird.bird import Bird
from flappybird.pipe import Pipe
from flappybird.score import Score
from typing import Optional, Tuple


class Game:
    def __init__(self, mode: str, surface: Optional[pygame.Surface] = None,
                 width: int = 423, height: int = 590, headless: bool = False):
        """
        Core game controller.

        Args:
            mode (str): "human" or "ai".
            surface (pygame.Surface|None): display surface (None if headless).
            width (int): screen width.
            height (int): screen height.
            headless (bool): draw into an off-screen surface if True.
        """
        self.mode = mode
        self.headless = bool(headless)
        self.screen_width = width
        self.screen_height = height
        self.surface = surface if surface and not self.headless else pygame.Surface((width, height))

        self.bird = Bird(mode)
        self.pipes = []
        self.pipe_spawn_timer = 0
        
        self.base_sprite = self._load_image("assets/sprites/base.png", alpha=True)
        self.base_scroll_speed = 3
        self.base_width = self.base_sprite.get_width()
        self.base_x = 0
        self.base_y = self.screen_height - self.base_sprite.get_height() + 20

        bg_original = self._load_image("assets/sprites/background-day.png", alpha=False)
        self.bg_scaled_height = int(self.screen_height * 1.2)
        self.background = pygame.transform.scale(bg_original, (self.screen_width, self.bg_scaled_height))

        self.game_over_sprite_original = self._load_image("assets/sprites/gameover.png", alpha=True)
        self.game_over_sprite = pygame.transform.scale(
            self.game_over_sprite_original,
            (int(self.game_over_sprite_original.get_width() * 1.3),
             int(self.game_over_sprite_original.get_height() * 1.3))
        )
        get_ready_original = self._load_image("assets/sprites/message.png", alpha=True)
        gr_w, gr_h = get_ready_original.get_size()
        self.get_ready_sprite = pygame.transform.scale(get_ready_original, (int(gr_w * 1.4), int(gr_h * 1.4)))

        self.panel_score_sprite_original = self._load_image("assets/sprites/panel_score.png", alpha=True)
        self.panel_score_sprite = pygame.transform.scale(
            self.panel_score_sprite_original,
            (int(self.panel_score_sprite_original.get_width() * 2.7),
             int(self.panel_score_sprite_original.get_height() * 2.7))
        )
        self.panel_score_x = (self.screen_width - self.panel_score_sprite.get_width()) // 2
        self.panel_score_y = (self.screen_height - self.panel_score_sprite.get_height()) // 2
        self.draw_result = False

        self.score = Score()
        self.current_score = 0
        self.best_score = self.load_best_score()
        self.new_best_score = False

        self.button_ok_original = self._load_image("assets/sprites/button_ok.png", alpha=True)
        self.button_ok = pygame.transform.scale(
            self.button_ok_original,
            (int(self.button_ok_original.get_width() * 2),
             int(self.button_ok_original.get_height() * 2))
        )
        self.button_ok_x = self.screen_width // 2 - self.button_ok.get_width() // 2 
        self.button_ok_y = self.panel_score_y + self.panel_score_sprite.get_height() + 20

        self.label_new_original = self._load_image("assets/sprites/label_new.png", alpha=True)
        self.label_new = pygame.transform.scale(
            self.label_new_original,
            (int(self.label_new_original.get_width() * 2),
             int(self.label_new_original.get_height() * 2))
        )

        self.waiting_to_start = True
        self.game_over = False
        self.played_die_sound = False
        self.penality = 0
        self.reward = 0

        self.sfx_die = self._load_sound("assets/audio/die.wav")
        self.sfx_jump = self._load_sound("assets/audio/wing.wav")
        self.sfx_point = self._load_sound("assets/audio/point.wav")
        self.sfx_swoosh = self._load_sound("assets/audio/swoosh.wav")
        self.sfx_hit = self._load_sound("assets/audio/hit.wav")

    def reset(self) -> None:
        """Reset game objects to start a new round."""
        self.bird.reset()
        self.pipes.clear()
        self.score.scale(0.9)
        self.current_score = 0
        if self.mode == "ai":
            self.waiting_to_start = False
        else:
            self.waiting_to_start = True
        self.game_over = False
        self.played_die_sound = False
        self.pipe_spawn_timer = 0
        self.new_best_score = False
        self.medal = None

    def update(self) -> Tuple[float, bool]:
        """Run one frame of game logic and rendering."""
        self.surface.blit(self.background, (0, -60))

        if self.mode == "human" and self.waiting_to_start:
            self.bird.jump()
            self.draw_get_ready()
            self.update_base()
            self.draw_base()
            return 0.0, False

        # Game Over screen
        if self.game_over and self.mode == "human":
            self.bird.update()

            # Stop bird on ground
            if self.bird.get_rect().bottom >= self.base_y:
                self.bird.y = self.base_y - self.bird.get_rect().height
                self.bird.velocity = 0

            # Draw everything
            self.draw_pipes()
            self.bird.draw(self.surface)
            self.draw_base()
            self.draw_game_over()

            self.draw_panel_score(self.panel_score_x, self.panel_score_y)
            self.score.scale(0.6)
            self.panel_score_pos_x = self.panel_score_x + int(self.panel_score_sprite.get_width() * 0.86)
            self.panel_score_pos_y = self.panel_score_y + int(self.panel_score_sprite.get_height() * 0.32)
            self.score.draw(self.surface, self.current_score, self.panel_score_pos_x, self.panel_score_pos_y)
        
            self.medal = self.select_medal(self.current_score)
            if self.medal:
                medal_x = self.panel_score_x + int(self.panel_score_sprite.get_width() * 0.125)
                medal_y = self.panel_score_y + int(self.panel_score_sprite.get_height() * 0.40)
                self.draw_medal(medal_x, medal_y)

            # Save best score
            if self.current_score > self.best_score:
                self.best_score = self.current_score
                self.new_best_score = True
                self.save_best_score()

            self.score.draw(self.surface, self.best_score, self.panel_score_pos_x, self.panel_score_pos_y + int(self.panel_score_sprite.get_height() * 0.36))
            if self.new_best_score:
                self.panel_new_x = self.panel_score_x - 70
                self.panel_new_y = self.panel_score_y + int(self.panel_score_sprite.get_height() * 0.218)
                self.draw_label_new(self.panel_new_x, self.panel_new_y)
                self.draw_ok_button(self.button_ok_x, self.button_ok_y)

            # Play die sound once
            if not self.played_die_sound and self.sfx_die:
                self.sfx_die.play()
                self.played_die_sound = True

            return -1.0, True
        

        self.pipe_spawn_timer += 1
        if self.pipe_spawn_timer >= 80:
            self.spawn_pipe()
            self.pipe_spawn_timer = 0

        self.bird.update()
        self.update_pipes()
        self.update_base()

        if not self.headless:
            self.draw_pipes()
            self.bird.draw(self.surface)
            self.draw_base()
            self.score.draw(self.surface, self.current_score, self.screen_width // 2, 30)

        if self.check_collision():
            if self.sfx_hit:
                self.sfx_hit.play()
            self.game_over = True
            return -10.0 + self.penality, True
        
        
        return 0.1, False
    
    def select_medal(self, score: int) -> Optional[pygame.Surface]:
        """Return the medal sprite corresponding to the score.

        Args:
            score (int): The player's score.

        Returns:
            pygame.Surface or None: The medal sprite, or None if no medal.
        """
        medals = [
            (40, "assets/sprites/medal_platinum.png"),
            (30, "assets/sprites/medal_gold.png"),
            (20, "assets/sprites/medal_silver.png"),
            (10, "assets/sprites/medal_bronze.png"),
        ]

        for threshold, path in medals:
            if score >= threshold:
                medal = self._load_image(path, alpha=True)
                scale_factor = 0.18
                width = int(self.panel_score_sprite.get_width() * scale_factor)
                height = int(medal.get_height() * (width / medal.get_width()))
                return pygame.transform.scale(medal, (width, height))

        return None
    
    def draw_base(self) -> None:
        """Tile the base sprite across the bottom."""
        for i in range((self.screen_width // self.base_width) + 2):
            self.surface.blit(self.base_sprite, (self.base_x + i * self.base_width, self.base_y))

    def draw_game_over(self) -> None:
        """Draw the Game Over banner centered."""
        x = (self.screen_width - self.game_over_sprite.get_width()) // 2
        y = self.screen_height // 5
        self.surface.blit(self.game_over_sprite, (x, y))

    def draw_label_new(self, x: int, y: int) -> None:
        """Draw the 'New' label at the specified position."""
        self.surface.blit(self.label_new, (x, y))
    
    def draw_pipes(self) -> None:
        """Draw all pipes."""
        for pipe in self.pipes:
            pipe.draw(self.surface)
    
    def draw_get_ready(self) -> None:
        """Draw the 'Get Ready' prompt centered near the top."""
        x = (self.screen_width - self.get_ready_sprite.get_width()) // 2
        y = self.screen_height // 8
        self.surface.blit(self.get_ready_sprite, (x, y))
    
    def draw_medal(self, x: int, y: int) -> None:
        """Draw the selected medal at the specified position.

        Args:
            x (int): The x-coordinate to draw the medal.
            y (int): The y-coordinate to draw the medal.
        """
        if self.medal:
            self.surface.blit(self.medal, (x, y))

    def draw_panel_score(self, x: int, y: int) -> None:
        """Draw the score panel at the specified position.

        Args:
            x (int): The x-coordinate to draw the panel.
            y (int): The y-coordinate to draw the panel.
        """
        self.surface.blit(self.panel_score_sprite, (x, y))

    def draw_ok_button(self, x: int, y: int) -> None:
        """Draw the OK button at the specified position.

        Args:
            x (int): The x-coordinate to draw the button.
            y (int): The y-coordinate to draw the button.
        """
        self.surface.blit(self.button_ok, (x, y))

    def update_pipes(self) -> float:
        """Move pipes left, mark passed pipes, and remove off-screen ones."""
        self.reward = 0
        for pipe in self.pipes:
            pipe.update()
            if not pipe.passed and pipe.x + (pipe.width / 4) < self.bird.x:
                pipe.passed = True
                self.current_score += 1
                self.reward = 10
                if self.sfx_point:
                    self.sfx_point.play()
        self.pipes = [p for p in self.pipes if p.x + p.width > 0]
        return self.reward

    def update_base(self) -> None:
        """Scroll base texture horizontally."""
        self.base_x -= self.base_scroll_speed
        if self.base_x <= -self.base_width:
            self.base_x = 0

    def check_collision(self) -> bool:
        """Return True if bird collides with ground, ceiling, or pipes."""
        self.penality = 0
        bird_rect = self.bird.get_rect()
        if bird_rect.bottom >= self.base_y:
            self.penality = -100
            self.bird.y = self.base_y - bird_rect.height
            return True
        if bird_rect.top <= 0:
            self.penality = -100
            return True
        for pipe in self.pipes:
            top_rect, bottom_rect = pipe.get_rects()
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                return True
        return False

    def spawn_pipe(self) -> None:
        """Create a new pipe at right edge."""
        self.pipes.append(Pipe(x=self.screen_width))

    def load_best_score(self) -> int:
        """Load best score from disk safely."""
        try:
            with open("flappybird/score.json", "r") as f:
                data = json.load(f)
                return data.get("best_score", 0)
        except Exception:
            return 0

    def save_best_score(self) -> None:
        """Save best score to disk safely."""
        try:
            with open("flappybird/score.json", "w") as f:
                json.dump({"best_score": self.best_score}, f)
        except Exception:
            pass

    @staticmethod
    def _load_image(path: str, alpha: bool = True) -> pygame.Surface:
        """Load an image safely; fallback to 1x1 surface if missing."""
        try:
            img = pygame.image.load(path)
            return img.convert_alpha() if alpha else img.convert()
        except Exception:
            return pygame.Surface((1, 1), flags=pygame.SRCALPHA if alpha else 0)

    @staticmethod
    def _load_sound(path: str) -> Optional[pygame.mixer.Sound]:
        """Load a sound safely; return None if missing."""
        try:
            return pygame.mixer.Sound(path)
        except Exception:
            return None
