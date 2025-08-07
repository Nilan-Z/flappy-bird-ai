import pygame
import sys
from flappybird.game import Game

pygame.init()

SCREEN_WIDTH = 423
SCREEN_HEIGHT = 590

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird AI")

game = Game(window)
clock = pygame.time.Clock()

def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
            if game.waiting_to_start:
                game.waiting_to_start = False
                game.bird.gravity = 0.25
                game.bird.jump()
                game.sfx_jump.play()
            else:
                game.bird.jump()
                game.sfx_jump.play()

def main_loop():
    while True:
        handle_input()

        if not game.waiting_to_start and not game.game_over:
            game.bird.update()

        game.update()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_loop()
