import pygame
import json
from flappybird.bird import Bird
from flappybird.pipe import Pipe
from flappybird.score import Score


class Game:
    def __init__(self, mode, surface=None, width=423, height=590, headless=False):
        """
        Core game controller.

        Args:
            mode (str): "human" or "ai".
            surface (pygame.Surface|None): display surface (None if headless).
            width (int): screen width (used if headless or surface is None).
            height (int): screen height.
            headless (bool): when True, draw into an off-screen surface.
        """
        self.mode = mode
        self.headless = bool(headless)

        # screen size
        self.screen_width = width
        self.screen_height = height

        # surface: use provided surface when available and not running headless
        if not self.headless and surface is not None:
            self.surface = surface
        else:
            # off-screen surface for headless mode or missing surface
            self.surface = pygame.Surface((self.screen_width, self.screen_height))

        # game objects
        self.bird = Bird(mode)
        self.pipes = []
        self.pipe_spawn_timer = 0

        # load images with safe fallbacks (avoid crashing if load fails)
        def _load_image(path, alpha=True):
            try:
                img = pygame.image.load(path)
                return img.convert_alpha() if alpha else img.convert()
            except Exception:
                # return a plain surface as fallback
                fallback = pygame.Surface((1, 1), flags=pygame.SRCALPHA if alpha else 0)
                return fallback

        # base (ground)
        self.base_sprite = _load_image("assets/sprites/base.png", alpha=True)
        self.base_scroll_speed = 3
        self.base_width = self.base_sprite.get_width()
        self.base_x = 0
        self.base_y = self.screen_height - self.base_sprite.get_height() + 20

        # background
        self.bg_original = _load_image("assets/sprites/background-day.png", alpha=False)
        self.bg_scaled_height = int(self.screen_height * 1.2)
        try:
            self.background = pygame.transform.scale(self.bg_original, (self.screen_width, self.bg_scaled_height))
        except Exception:
            # fallback to a plain fill surface
            self.background = pygame.Surface((self.screen_width, self.bg_scaled_height))

        # UI: game over and get-ready
        self.game_over_sprite = _load_image("assets/sprites/gameover.png", alpha=True)
        self.get_ready_original = _load_image("assets/sprites/message.png", alpha=True)
        gr_w = self.get_ready_original.get_width()
        gr_h = self.get_ready_original.get_height()
        try:
            self.get_ready_sprite = pygame.transform.scale(self.get_ready_original, (int(gr_w * 1.4), int(gr_h * 1.4)))
        except Exception:
            self.get_ready_sprite = self.get_ready_original

        # score
        self.score = Score()
        self.current_score = 0
        self.best_score = self.load_best_score()

        # game state
        self.waiting_to_start = True
        self.game_over = False
        self.played_die_sound = False

        # sounds (load safely)
        def _load_sound(path):
            try:
                return pygame.mixer.Sound(path)
            except Exception:
                return None

        self.sfx_die = _load_sound("assets/audio/die.wav")
        self.sfx_jump = _load_sound("assets/audio/wing.wav")
        self.sfx_point = _load_sound("assets/audio/point.wav")

    def reset(self):
        """Reset game objects to start a new round."""
        self.bird.reset()
        self.pipes.clear()
        self.current_score = 0
        self.waiting_to_start = False
        self.game_over = False
        self.played_die_sound = False
        self.pipe_spawn_timer = 0

    def update(self):
        """
        Run one frame of game logic and rendering.

        Returns:
            (reward(float), done(bool))
        """
        # draw background first
        try:
            self.surface.blit(self.background, (0, -60))
        except Exception:
            pass

        # pre-start screen for human: show "get ready"
        if self.mode == "human" and self.waiting_to_start:
            self.bird.jump()
            self.draw_get_ready()
            self.update_base()
            self.draw_base()
            return 0.0, False

        # game over handling
        if self.game_over and self.mode == 'human':
            self.bird.update()
            self.bird.draw(self.surface)
            self.draw_pipes()
            self.draw_base()
            self.draw_game_over()
            time.wait(3)

            if self.current_score > self.best_score:
                self.best_score = self.current_score
                self.save_best_score()

            if not self.played_die_sound and self.sfx_die:
                try:
                    self.sfx_die.play()
                except Exception:
                    pass
                self.played_die_sound = True

            # draw score
            try:
                self.score.draw(self.surface, self.current_score, self.screen_width // 2, self.screen_height // 2)
            except Exception:
                pass

            return -1.0, True

        # main gameplay loop
        self.pipe_spawn_timer += 1
        if self.pipe_spawn_timer >= 80:
            self.spawn_pipe()
            self.pipe_spawn_timer = 0

        # bird
        self.bird.update()
        self.bird.draw(self.surface)

        # pipes and base
        self.update_pipes()
        self.draw_pipes()
        self.update_base()
        self.draw_base()

        # score HUD
        try:
            self.score.draw(self.surface, self.current_score, self.screen_width // 2, 30)
        except Exception:
            pass

        # collisions
        if self.check_collision():
            self.game_over = True
            self.bird.velocity = 0
            return -10.0 + self.penality, True

        return 0.1, False

    def update_pipes(self):
        """Move pipes left, mark passed pipes and remove off-screen ones."""
        for pipe in self.pipes:
            pipe.update()
            if not pipe.passed and pipe.x + (pipe.width / 4) < self.bird.x:
                pipe.passed = True
                self.current_score += 1
                if self.sfx_point:
                    try:
                        self.sfx_point.play()
                    except Exception:
                        pass
        self.pipes = [p for p in self.pipes if p.x + p.width > 0]

    def draw_pipes(self):
        """Draw all pipes to the surface."""
        for pipe in self.pipes:
            pipe.draw(self.surface)

    def update_base(self):
        """Scroll base texture horizontally."""
        self.base_x -= self.base_scroll_speed
        if self.base_x <= -self.base_width:
            self.base_x = 0

    def draw_base(self):
        """Tile the base sprite across the bottom."""
        try:
            self.surface.blit(self.base_sprite, (self.base_x, self.base_y))
            self.surface.blit(self.base_sprite, (self.base_x + self.base_width, self.base_y))
            self.surface.blit(self.base_sprite, (self.base_x + self.base_width * 2, self.base_y))
        except Exception:
            pass

    def draw_game_over(self):
        """Draw the Game Over banner centered."""
        try:
            x = (self.screen_width - self.game_over_sprite.get_width()) // 2
            y = self.screen_height // 4
            self.surface.blit(self.game_over_sprite, (x, y))
        except Exception:
            pass

    def check_collision(self):
        """Return True if bird collides with ground, ceiling or pipes."""
        bird_rect = self.bird.get_rect()
        if bird_rect.bottom >= self.base_y:
            self.penality = -100
            return True
        if bird_rect.top <= 0:
            self.penality = -100
            return True
        for pipe in self.pipes:
            top_rect, bottom_rect = pipe.get_rects()
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                return True
        return False

    def draw_get_ready(self):
        """Draw the 'Get Ready' prompt centered near the top."""
        try:
            x = (self.screen_width - self.get_ready_sprite.get_width()) // 2
            y = self.screen_height // 8
            self.surface.blit(self.get_ready_sprite, (x, y))
        except Exception:
            pass

    def spawn_pipe(self):
        """Create a new pipe at right edge."""
        self.pipes.append(Pipe(x=self.screen_width))

    def load_best_score(self):
        """Load best score from disk (safe)."""
        try:
            with open("flappybird/score.json", "r") as f:
                data = json.load(f)
                return data.get("best_score", 0)
        except Exception:
            return 0

    def save_best_score(self):
        """Save best score to disk (safe)."""
        try:
            with open("flappybird/score.json", "w") as f:
                json.dump({"best_score": self.best_score}, f)
        except Exception:
            pass
