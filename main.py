import pygame
import sys
from flappybird.game import Game

pygame.init()

width = 288     
height = 512    #Original dimensions of Flappy Bird
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("flappy-bird-ai")

game = Game(window)
clock = pygame.time.Clock()


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game.update()
        pygame.display.flip()
        clock.tick(60)
