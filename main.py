import pygame
import sys
from flappybird.game import Game

pygame.init()

SCREEN_WIDTH = 423
SCREEN_HEIGHT = 590

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird AI")
pygame.display.set_icon(pygame.image.load("assets/sprites/yellowbird-upflap.png").convert_alpha())

game = Game(window)
clock = pygame.time.Clock()


def handle_input():
    """
    Process all user input events.

    Handles quitting the game, starting the game from the waiting state,
    and triggering the bird's jump on spacebar press or mouse click.
    Plays the jump sound effect when the bird jumps.

    This function polls the pygame event queue each frame.
    """
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


def main_loop():
    """
    Main game loop that runs continuously until the program is exited.

    This loop:
    - Processes user inputs
    - Updates the bird only when the game is running (not waiting or over)
    - Updates game state
    - Refreshes the display
    - Caps the frame rate at 60 FPS
    """
    while True:
        handle_input()

        if not game.waiting_to_start and not game.game_over:
            game.bird.update()

        game.update()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_loop()
