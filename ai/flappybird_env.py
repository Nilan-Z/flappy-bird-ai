import pygame
from flappybird.game import Game
from main import SCREEN_WIDTH, SCREEN_HEIGHT

class FlappyBirdEnv:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird AI")

        self.game = Game(self.screen, user="ai")
        self.clock = pygame.time.Clock()

        self.bird = self.game.bird
        self.pipes = self.game.pipes

    def reset(self):
        self.game.reset()
        self.game.waiting_to_start = False
        self.bird = self.game.bird
        self.pipes = self.game.pipes
        return self.get_state()

    def step(self, action):
        if action == 1:
            self.bird.jump()

        self.game.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self.get_state(), -1, True, {}

        pygame.display.flip()
        self.clock.tick(30)

        next_state = self.get_state()
        reward = self.compute_reward()
        done = self.game.game_over

        return next_state, reward, done, {}

    def get_state(self):
        bird_y = self.bird.y
        bird_vel = self.bird.velocity

        pipe = None
        for p in self.pipes:
            if p.x + p.width > self.bird.x:
                pipe = p
                break

        if pipe is None:
            pipe_dist = 0
            pipe_top = 0
            pipe_bottom = 0
        else:
            pipe_dist = pipe.x - self.bird.x
            pipe_top = pipe.top_height
            pipe_bottom = pipe.bottom_height

        return [bird_y, bird_vel, pipe_dist, pipe_top, pipe_bottom]

    def compute_reward(self):
        if self.game.game_over:
            return -1.0
        else:
            return 0.1

    def render(self):
        pygame.display.flip()
