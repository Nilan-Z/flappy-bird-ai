import pygame
import sys
from flappybird.game import Game

if __name__ == "__main__":
    pygame.init()
    game = Game()
    clock = pygame.time.Clock()

    width = 288     
    height = 512    #Original dimensions of Flappy Bird
    fenetre = pygame.display.set_mode((width, height))
    pygame.display.set_caption("flappy-bird-ai")



    while True:
        #Future game logic will go here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.flip()
        clock.tick(60)
