import pygame
import sys
from pygame import *

import pygooey

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
        self.money = 1000000

        self.menu()
        self.loop()


    def loop(self):
        About = False
        Game = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.sbrect.collidepoint(x, y):
                        print('Wlaczono instrukcje')
                        self.screen.fill((0, 0, 0))
                        self.sbrect = pygame.Rect((-1, -1), (0, 0))
                        pygame.display.update()
                        About = True
                        self.about()

                keys = pygame.key.get_pressed()
                if About==True:
                    if event.type == pygame.KEYDOWN:
                        if keys[pygame.K_SPACE]:
                            print('Rozpoczato gre')
                            About = False
                            Game = True

                            self.game()
                            pygame.display.update()
                if Game==True:
                    self.entry1 .get_event(event)
            if Game == True:
                self.entry1.update()
                self.entry1.draw(self.screen)
            pygame.display.update()

    def menu(self):
        self.screen.fill((0, 0, 0))
        bg = pygame.image.load('Img/main.jpg').convert()
        bg = pygame.transform.scale(bg, (BG_WIDTH, BG_HEIGHT))
        self.screen.blit(bg, (0, 0))
        self.x = BG_WIDTH / 2 - BT_WIDTH / 2
        self.y = BG_HEIGHT - BG_HEIGHT / 4

        self.sb = pygame.image.load('Img/button.png')
        self.sb = pygame.transform.scale(self.sb, (BT_WIDTH, BT_HEIGHT))
        self.sbrect = pygame.Rect((self.x, self.y),(BT_WIDTH, BT_HEIGHT))
        self.screen.blit(self.sb, (self.x, self.y))


        pygame.display.update()

    def about(self):
        self.screen.fill((71, 209, 255))
        myfont = pygame.font.SysFont("monospace", 40)
        label = myfont.render("Instrukcja", 1, (255, 255, 0))
        label2 = myfont.render("Nacisnij [SPACJA], zeby rozpoczac", 1, (255, 255, 0))
        self.screen.blit(label, (BG_WIDTH/2-120, 50))
        self.screen.blit(label2, (60, BG_HEIGHT-BG_HEIGHT/4))
        pygame.display.update()

    def game(self):

        bg = pygame.image.load('Img/ss.jpg').convert()
        bg = pygame.transform.scale(bg, (BG_WIDTH, BG_HEIGHT))
        self.screen.blit(bg, (0, 0))
        settings = {
            "command": self.print_on_enter,
            "inactive_on_enter": False,
            "aaccepted": " "
        }
        self.entry1 = pygooey.TextBox(rect=(70, 100, 150, 30), **settings, id="1")
        self.entry2 = pygooey.TextBox(rect=(70, 200, 150, 30), **settings, id="2")
        self.entry3 = pygooey.TextBox(rect=(70, 300, 150, 30), **settings, id="3")
        self.entry4 = pygooey.TextBox(rect=(70, 400, 150, 30), **settings, id="4")
        pygame.display.update()


    def print_on_enter(self, id, final):
        print(format(final)+id)






Game()