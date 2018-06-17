import pygame,sys
from pygame import  *

class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

        bg = pygame.image.load('logo.jpg')
        self.screen.fill((0, 0, 0))
        self.screen.blit(bg, (0, 0))
        self.wait()

    def wait(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return


