import pygame
from flappybird.game import Game

class FlappyBirdEnv:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((288, 512))
        pygame.display.set_caption("Flappy Bird AI")

        self.game = Game(self.screen)
        self.clock = pygame.time.Clock()

    def reset(self):
        self.game = Game(self.screen)
        return self.get_state()

    def step(self, action):
        if action == 1:
            self.game.bird.jump()

        self.game.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()
        self.clock.tick(30)

        next_state = self.get_state()
        reward = self.compute_reward()
        done = self.game.game_over

        return next_state, reward, done, {}

    def get_state(self):
        bird_y = self.game.bird.y
        bird_vel = self.game.bird.velocity
        pipe = None
        for p in self.game.pipes:
            if p.x + p.width > self.game.bird.x:
                pipe = p
                break
        if pipe is None:
            pipe_dist = 0
            pipe_top = 0
            pipe_bottom = 0
        else:
            pipe_dist = pipe.x - self.game.bird.x
            pipe_top = pipe.top_height
            pipe_bottom = pipe.bottom_height

        return [bird_y, bird_vel, pipe_dist, pipe_top, pipe_bottom]

    def compute_reward(self):
        if self.game.game_over:
            return -1
        else:
            return 0.1
        
    def render(self):
        pygame.display.flip()

