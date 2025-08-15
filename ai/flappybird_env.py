import pygame
import yaml
from flappybird.game import Game




class FlappyBirdEnv:
    """
    Flappy Bird environment for AI training or human play.
    Provides Gym-style methods: reset(), step(), render().
    """
    def __init__(self, mode="ai"):
        """
        Initialize the environment.

        Args:
            mode (str): "ai" for AI control, "human" for manual keyboard control.
        """
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)

        SCREEN_WIDTH = config["screen_width"]
        SCREEN_HEIGHT = config["screen_height"]

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()

        self.mode = mode
        self.game = Game(self.screen, user=mode)

        # Direct references for faster access
        self.bird = self.game.bird
        self.pipes = self.game.pipes

    

    def reset(self):
        """
        Fully reset the game state.

        Returns:
            list: Initial observation [bird_y, bird_velocity, pipe_distance, pipe_top, pipe_bottom].
        """
        self.game.reset()
        self.bird = self.game.bird
        self.pipes = self.game.pipes
        return self.get_state()

    def step(self, action):
        """
        Perform one step in the game.

        Args:
            action (int or None):
                1 = jump, 0 = do nothing
        Returns:
            tuple: (next_state, reward, done, info)
        """
        # AI control
        if action == 1:
            self.bird.jump()
        # Update game logic
        reward, done = self.game.update_logic()

        return self.get_state(), reward, done, {}

    def get_state(self):
        """
        Build the observation for AI training.

        Returns:
            list: [bird_y, bird_velocity, pipe_distance, pipe_top, pipe_bottom]
        """
        bird_y = self.bird.y
        bird_vel = self.bird.velocity

        # Find the next pipe in front of the bird
        pipe = next((p for p in self.pipes if p.x + p.width > self.bird.x), None)

        if pipe is None:
            pipe_dist = 0
            pipe_top = 0
            pipe_bottom = 0
        else:
            top_rect, bottom_rect = pipe.get_rects()
            pipe_dist = pipe.x - self.bird.x
            pipe_top = top_rect
            pipe_bottom = bottom_rect

        return [bird_y, bird_vel, pipe_dist, pipe_top, pipe_bottom]

    def render(self):
        """
        Render the current game frame and maintain the framerate.
        """
        pygame.display.flip()
        self.clock.tick(30)

    def close(self):
        """
        Close the Pygame window.
        """
        pygame.quit()
