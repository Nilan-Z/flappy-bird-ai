import sys
import argparse
import pygame
import yaml
from flappybird.game import Game
from ai.flappybird_env import FlappyBirdEnv
from ai.train import TrainAgent  


with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

SCREEN_WIDTH = config["screen_width"]
SCREEN_HEIGHT = config["screen_height"]

def run_human():
    """Run the game in manual (human) mode."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird - Human Mode")
    pygame.display.set_icon(pygame.image.load("assets/sprites/yellowbird-upflap.png").convert_alpha())

    game = Game(screen, user="human")
    clock = pygame.time.Clock()

    while True:
        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                if game.waiting_to_start:
                    game.waiting_to_start = False
                elif not game.game_over:
                    game.bird.jump()
                    game.sfx_jump.play()

        if not game.waiting_to_start and not game.game_over:
            game.bird.update()

        game.update_logic()
        pygame.display.flip()
        clock.tick(60)


def run_ai(train=False):
    """Run the game in AI mode."""
    env = FlappyBirdEnv(mode="ai")

    if train:
        print("Starting AI training...")
        TrainAgent.train(episodes=500)
    else:
        print("Running AI without training...")
        pass

    env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flappy Bird - Human or AI Mode")
    parser.add_argument("user", choices=["human", "ai"], help="Select mode: 'human' for manual play or 'ai' for AI control")
    parser.add_argument("--train", action="store_true", help="If set with 'ai' mode, starts training instead of running")
    args = parser.parse_args()

    if args.user == "human":
        run_human()
    elif args.user == "ai":
        run_ai(train=args.train)
