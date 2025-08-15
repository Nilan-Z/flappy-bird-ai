import sys
import argparse
import pygame
import yaml
from flappybird.game import Game
from ai.flappybird_env import FlappyBirdEnv
from ai.train import TrainAgent  

# Load game configuration from YAML file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

SCREEN_WIDTH = config["screen_width"]
SCREEN_HEIGHT = config["screen_height"]

def run_human():
    """
    Launch the game in player-controlled mode.
    Initializes Pygame, loads assets, and processes real-time input.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird - Human Mode")
    pygame.display.set_icon(pygame.image.load("assets/sprites/yellowbird-upflap.png").convert_alpha())

    game = Game(screen, user="human")
    clock = pygame.time.Clock()
    game.waiting_to_start = True

    while True:
        # Event loop for handling keyboard and mouse actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Start game or trigger bird jump
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                if game.waiting_to_start:
                    game.waiting_to_start = False
                elif not game.game_over:
                    game.bird.jump()
                    game.sfx_jump.play()

        # Allow bird idle animation before game starts
        if not game.waiting_to_start and not game.game_over:
            game.bird.update()

        game.update()
        pygame.display.flip()
        clock.tick(60)  # Limit frame rate


def run_ai(train=False):
    """
    Launch the game in AI mode.
    Can either run an already trained agent or start a training session.
    """
    env = FlappyBirdEnv(mode="ai")

    if train:
        print("Starting AI training...")
        TrainAgent.train(episodes=500)
    else:
        print("Running AI without training...")
        pass

    env.close()


if __name__ == "__main__":
    # Command-line interface to select mode and options
    parser = argparse.ArgumentParser(description="Flappy Bird - Human or AI Mode")
    parser.add_argument("user", choices=["human", "ai"], help="Choose control type: 'human' or 'ai'")
    parser.add_argument("--train", action="store_true", help="Use with 'ai' to enable training mode")
    args = parser.parse_args()

    if args.user == "human":
        run_human()
    elif args.user == "ai":
        run_ai(train=args.train)
