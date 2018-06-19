import pygame
from pygame import *

BG_WIDTH = 900
BG_HEIGHT = 600
BT_WIDTH=350
BT_HEIGHT=120

class Game(object):

    def __init__(self):
        #inicjalizcja nowej gry
        pygame.init()
        self.screen = pygame.display.set_mode((BG_WIDTH, BG_HEIGHT))
        pygame.display.set_caption('Postaw na milion')
        self.gameIcon = pygame.image.load('Img\mainLogo.png')
        pygame.display.set_icon(self.gameIcon)

        self.menu()
        self.loop()


    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.sbrect.collidepoint(x, y):
                        print('Rozpoczeto gre')
                        self.screen.fill((0, 0, 0))
                        pygame.display.update()
    def menu(self):
        bg = pygame.image.load('Img/logo.jpg').convert()
        bg = pygame.transform.scale(bg, (BG_WIDTH, BG_HEIGHT))

        self.screen.blit(bg, (0, 0))
        self.sb = pygame.image.load('Img/button.png')
        self.sb = pygame.transform.scale(self.sb, (BT_WIDTH, BT_HEIGHT))
        self.x = BG_WIDTH/2-BT_WIDTH/2
        self.y = BG_HEIGHT-BG_HEIGHT/4
        self.screen.blit(self.sb, (self.x, self.y))
        self.sbrect = pygame.Rect((self.x, self.y),(BT_WIDTH, BT_HEIGHT))
        pygame.display.update()





Game()
