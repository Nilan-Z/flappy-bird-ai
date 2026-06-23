import os
import pygame
from typing import List, Tuple, Dict, Any
from flappybird.game import Game
from flappybird.path_utils import load_yaml_config


# Load config only once at module level (avoid re-reading config.yaml every instance)
CONFIG = load_yaml_config()


class FlappyBirdEnv:
    def __init__(self, mode: str = "ai", headless: bool = False):
        """
        Flappy Bird environment for RL.

        Args:
            mode: "ai" or "human"
            headless: if True, run without visible window
        """
        self.mode = mode
        self.headless = bool(headless)

        # Load screen parameters from config.yaml
        self.SCREEN_WIDTH = int(CONFIG.get("screen_width", 423))
        self.SCREEN_HEIGHT = int(CONFIG.get("screen_height", 590))

        # Setup SDL dummy driver for headless mode
        if self.headless:
            os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

        # Initialize pygame
        pygame.init()

        self._created_dummy_display = False
        if self.headless:
            # Try to create a tiny dummy display so convert() still works
            try:
                pygame.display.init()
                pygame.display.set_mode((1, 1))
                self._created_dummy_display = True
            except Exception:
                pass
            self.screen = None
        else:
            # Create visible game window
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            pygame.display.set_caption("Flappy Bird (env)")

        # Game clock (fixed timestep)
        self.clock = pygame.time.Clock()

        # Instantiate Game (supporting possible different signatures)
        try:
            self.game = Game(
                mode=self.mode,
                surface=self.screen,
                width=self.SCREEN_WIDTH,
                height=self.SCREEN_HEIGHT,
                headless=self.headless,
            )
        except TypeError:
            self.game = Game(self.mode, self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.headless)

        # Shortcuts to in-game objects
        self.bird = getattr(self.game, "bird", None)
        self.pipes = getattr(self.game, "pipes", [])

    def reset(self) -> List[float]:
        """Reset the game and return initial state."""
        self.game.reset()
        self.bird = self.game.bird
        self.pipes = self.game.pipes
        return self.get_state()

    def step(self, action: int) -> Tuple[List[float], float, bool, Dict[str, Any]]:
        """
        Advance the game by one step.

        Args:
            action: 0 = no-op, 1 = jump

        Returns:
            state, reward, done, info
        """
        if action == 1 and hasattr(self.bird, "jump"):
            self.bird.jump()

        reward, done = self.game.update()
        return self.get_state(), reward, done, {}

    def get_state(self) -> List[float]:
        """
        Build simple observation:
        [bird_y, bird_velocity, pipe_distance, pipe_top_y, pipe_bottom_y]
        """
        bird_y = getattr(self.bird, "y", 0)
        bird_vel = getattr(self.bird, "velocity", 0)

        # Find the next pipe ahead of the bird
        next_pipe = next(
            (p for p in (self.pipes or [])
             if getattr(p, "x", 0) + getattr(p, "width", 0) > getattr(self.bird, "x", 0)),
            None,
        )

        if next_pipe:
            # Use safe fallback if get_rects() is not available
            top_rect, bottom_rect = getattr(next_pipe, "get_rects", lambda: (None, None))()
            pipe_dist = getattr(next_pipe, "x", 0) - getattr(self.bird, "x", 0)
            pipe_top_y = getattr(top_rect, "bottom", 0) if top_rect else 0
            pipe_bottom_y = getattr(bottom_rect, "top", self.SCREEN_HEIGHT) if bottom_rect else self.SCREEN_HEIGHT
        else:
            pipe_dist, pipe_top_y, pipe_bottom_y = self.SCREEN_WIDTH, 0, self.SCREEN_HEIGHT

        return [bird_y, bird_vel, pipe_dist, pipe_top_y, pipe_bottom_y]

    def render(self) -> None:
        """Render current frame to the screen (no-op in headless)."""
        if not self.headless:
            pygame.display.flip()
        self.clock.tick(60)

    def close(self) -> None:
        """Cleanup pygame resources (safe for headless)."""
        if self._created_dummy_display:
            try:
                pygame.display.quit()
            except Exception:
                pass
        # Note: pygame.quit() is global and will affect all pygame instances
        pygame.quit()
