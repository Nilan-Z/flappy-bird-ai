import pygame
import sys
from flappybird.game import Game

pygame.init()

SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird AI")

game = Game(window)
clock = pygame.time.Clock()

if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_over:
                    pass  # Restart logic could be added here
                elif game.waiting_to_start:
                    game.waiting_to_start = False
                    game.bird.gravity = 0.25
                    game.bird.jump()
                else:
                    game.bird.jump()

        if not game.waiting_to_start and not game.game_over:
            game.bird.update()

        game.update()
        pygame.display.flip()
        clock.tick(60)
