import sys
import os
import argparse
import yaml
import pygame
from flappybird.game import Game
from ai.flappybird_env import FlappyBirdEnv
from ai.train import TrainAgent
from ai.dqn_agent import DQNAgent

# Headless mode for AI training without graphics
if "--headless" in sys.argv:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

# Load configuration
with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

SCREEN_WIDTH = int(cfg.get("screen_width", 423))
SCREEN_HEIGHT = int(cfg.get("screen_height", 590))


def run_human():
    """Run the game in human mode."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird - Human Mode")

    try:
        icon = pygame.image.load("assets/sprites/yellowbird-upflap.png").convert_alpha()
        pygame.display.set_icon(icon)
    except Exception:
        pass

    game = Game(mode="human", surface=screen, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

    clock = pygame.time.Clock()
    game.waiting_to_start = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                if game.waiting_to_start:
                    game.waiting_to_start = False
                    game.sfx_swoosh.play()
                elif not game.game_over:
                    game.bird.jump()
                    try:
                        game.sfx_jump.play()
                    except Exception:
                        pass

        if not game.waiting_to_start and not game.game_over:
            game.bird.update()

        game.update()
        pygame.display.flip()
        clock.tick(60)


def run_ai(train: int = 0, headless: bool = False):
    """Run the AI agent, optionally training it."""
    env = FlappyBirdEnv(mode="ai", headless=headless)

    if train > 0:
        trainer = TrainAgent(headless=headless)
        trainer.train(episodes=train)
    else:
        agent = DQNAgent(state_size=5, action_size=2, training=False)
        state = env.reset()
        done = False
        while not done:
            action = agent.act(state)
            state, _, done, _ = env.step(action)
            if not headless:
                env.render()

    env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flappy Bird - Human or AI Mode")
    parser.add_argument("mode", choices=["human", "ai"], help="Choose 'human' or 'ai'")
    parser.add_argument("--train", type=int, nargs="?", const=1, default=0,
                        help="Number of episodes to train (AI only)")
    parser.add_argument("--headless", action="store_true", help="Run without rendering (AI only)")
    args = parser.parse_args()

    if args.mode == "human":
        run_human()
    else:
        run_ai(train=args.train, headless=args.headless)
