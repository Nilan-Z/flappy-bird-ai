import os
import yaml
import pygame
from typing import List, Tuple, Dict
from flappybird.game import Game


class FlappyBirdEnv:
    def __init__(self, mode: str = "ai", headless: bool = False):
        """
        Initialize environment.

        Args:
            mode: "ai" or "human".
            headless: If True, attempt to run without opening a visible window.
        """
        self.mode = mode
        self.headless = bool(headless)

        # Load config (screen size)
        with open("config.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        self.SCREEN_WIDTH = int(cfg.get("screen_width", 288))
        self.SCREEN_HEIGHT = int(cfg.get("screen_height", 512))

        # If headless requested, set dummy driver before pygame.init()
        if self.headless:
            os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

        # Initialize pygame
        pygame.init()

        # In headless mode try to create a tiny display so image.convert* works
        self._created_dummy_display = False
        if self.headless:
            try:
                pygame.display.init()
                pygame.display.set_mode((1, 1))
                self._created_dummy_display = True
            except Exception:
                # If dummy display fails we keep going; some image ops may still work
                pass

        # Create visible surface only when not headless
        if not self.headless:
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            pygame.display.set_caption("Flappy Bird (env)")
        else:
            self.screen = None

        # Time keeping
        self.clock = pygame.time.Clock()

        # Create Game instance (try keyword args then positional fallback)
        try:
            self.game = Game(mode=self.mode, surface=self.screen, width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT, headless=self.headless)
        except TypeError:
            # positional fallback in case Game signature differs
            self.game = Game(self.mode, self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.headless)

        # Shortcuts to in-game objects
        self.bird = getattr(self.game, "bird", None)
        self.pipes = getattr(self.game, "pipes", [])

    def reset(self) -> List[float]:
        """Reset the game and return initial observation."""
        self.game.reset()
        self.bird = self.game.bird
        self.pipes = self.game.pipes
        return self.get_state()

    def step(self, action: int) -> Tuple[List[float], float, bool, Dict]:
        """
        Advance the game by one step.

        Args:
            action: 0 = do nothing, 1 = jump

        Returns:
            (next_state, reward, done, info)
        """
        if action == 1 and hasattr(self.bird, "jump"):
            self.bird.jump()

        reward, done = self.game.update()
        return self.get_state(), reward, done, {}

    def get_state(self) -> List[float]:
        """
        Build simple observation for agent:
        [bird_y, bird_velocity, pipe_distance, pipe_top_y, pipe_bottom_y]
        """
        bird_y = getattr(self.bird, "y", 0)
        bird_vel = getattr(self.bird, "velocity", 0)

        # find next pipe in front of the bird
        next_pipe = next((p for p in (self.pipes or []) if getattr(p, "x", 0) + getattr(p, "width", 0) > getattr(self.bird, "x", 0)), None)

        if next_pipe:
            try:
                top_rect, bottom_rect = next_pipe.get_rects()
                pipe_dist = getattr(next_pipe, "x", 0) - getattr(self.bird, "x", 0)
                pipe_top_y = getattr(top_rect, "bottom", 0)
                pipe_bottom_y = getattr(bottom_rect, "top", 0)
            except Exception:
                pipe_dist = getattr(next_pipe, "x", 0) - getattr(self.bird, "x", 0)
                pipe_top_y = 0
                pipe_bottom_y = self.SCREEN_HEIGHT
        else:
            pipe_dist = self.SCREEN_WIDTH
            pipe_top_y = 0
            pipe_bottom_y = self.SCREEN_HEIGHT

        return [bird_y, bird_vel, pipe_dist, pipe_top_y, pipe_bottom_y]

    def render(self) -> None:
        """Render current frame to the display (no-op in headless)."""
        if not self.headless:
            pygame.display.flip()
        # keep timing consistent
        self.clock.tick(30)

    def close(self) -> None:
        """Clean up pygame and any dummy display used for headless mode."""
        if getattr(self, "_created_dummy_display", False):
            try:
                pygame.display.quit()
            except Exception:
                pass
        pygame.quit()
