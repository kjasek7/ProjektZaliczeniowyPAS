import sys
import pickle
import pygame
from pygame import *
import client
import pygooey

BG_WIDTH = 900
BG_HEIGHT = 600
BT_WIDTH=250
BT_HEIGHT=120


class Game(object):

    def __init__(self):
        #inicjalizcja nowej gry
        pygame.init()
        self.screen = pygame.display.set_mode((BG_WIDTH, BG_HEIGHT))
        pygame.display.set_caption('Postaw na milion')
        self.gameIcon = pygame.image.load('Img\mainLogo.png')
        pygame.display.set_icon(self.gameIcon)
        self.myfont = pygame.font.SysFont("monospace", 40)
        self.fps_clock = pygame.time.Clock()

        self.client = client.Client()
        if(self.client.connect()):
            self.client.send_message('ID')
            self.start()


    def start(self):
        self.menu()
        self.loop()

    def loop(self):
        self.About = False
        self.Game = False
        self.koniecCzasu = False
        self.time = 0.0
        self.money = 1000000
        self.pole = {str(1):0,str(2):0,str(3):0,str(4):0}
        self.prawidlowa = str(2)
        self.postawiono = 0
        self.iloscPytan = 1

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.send_message("Kliknieto exit")
                    self.client.close()
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.sbrect.collidepoint(x, y):
                        self.client.send_message("Kliknieto start")
                        self.sbrect = pygame.Rect((-1, -1), (0, 0))
                        self.ebrect = pygame.Rect((-1, -1), (0, 0))
                        self.ibrect = pygame.Rect((-1, -1), (0, 0))
                        self.About = False
                        self.Game = True
                        self.pytanie()

                    elif self.ebrect.collidepoint(x, y):

                        self.sbrect = pygame.Rect((-1, -1), (0, 0))
                        self.ebrect = pygame.Rect((-1, -1), (0, 0))
                        self.ibrect = pygame.Rect((-1, -1), (0, 0))
                        self.client.send_message("Kliknieto exit")
                        sys.exit(0)

                    elif self.ibrect.collidepoint(x, y):
                        self.client.send_message("Kliknieto instrukcja")
                        self.sbrect = pygame.Rect((-1, -1), (0, 0))
                        self.ebrect = pygame.Rect((-1, -1), (0, 0))
                        self.ibrect = pygame.Rect((-1, -1), (0, 0))
                        self.About = True
                        self.Game = False
                        self.about()



                keys = pygame.key.get_pressed()

                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_SPACE]:
                        if self.About == True:
                            self.client.send_message("Rozpoczeto gre")
                            self.About = False
                            self.Game = True
                            self.pytanie()

                        if self.koniecCzasu == True:
                            self.koniecCzasu = False
                            self.start_ticks = pygame.time.get_ticks()
                            self.pytanie()


                if self.Game==True:
                    self.entry1.get_event(event)
                    self.entry2.get_event(event)
                    self.entry3.get_event(event)
                    self.entry4.get_event(event)
                    self.entry1.update()
                    self.entry1.draw(self.screen)
                    self.entry2.update()
                    self.entry2.draw(self.screen)
                    self.entry3.update()
                    self.entry3.draw(self.screen)
                    self.entry4.update()
                    self.entry4.draw(self.screen)




            if self.Game == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.zbrect.collidepoint(x, y):
                        self.zlicz()
                        if int(self.postawiono) == int(self.money):
                            self.koniecCzasu = True
                            self.zbrect = pygame.Rect((-1, -1), (0, 0))
                            self.sprawdza()
                        else:
                            self.render_multi_line("Zle postawiles pieniadze!", BG_WIDTH / 2 - 50, 420, 15)
                seconds = round((pygame.time.get_ticks() - self.start_ticks) / 1000,0)

                self.updateClock(seconds)
                self.update()

            #self.fps_clock.tick(60)

            pygame.display.update()

    def menu(self):
        self.screen.fill((0, 0, 0))
        bg = pygame.image.load('Img/main.jpg').convert()
        bg = pygame.transform.scale(bg, (BG_WIDTH, BG_HEIGHT))
        self.screen.blit(bg, (0, 0))

        y = BG_HEIGHT - BG_HEIGHT / 4

        self.sb = pygame.image.load('Img/button.png')
        self.sb = pygame.transform.scale(self.sb, (BT_WIDTH, BT_HEIGHT))
        self.sbrect = pygame.Rect((0, y),(BT_WIDTH, BT_HEIGHT))
        self.screen.blit(self.sb, (0, y))

        self.ib = pygame.image.load('Img/buttoni.png')
        self.ib = pygame.transform.scale(self.ib, (BT_WIDTH, BT_HEIGHT))
        self.ibrect = pygame.Rect((325, y), (BT_WIDTH, BT_HEIGHT))
        self.screen.blit(self.ib, (325, y))

        self.eb = pygame.image.load('Img/buttone.png')
        self.eb = pygame.transform.scale(self.eb, (BT_WIDTH, BT_HEIGHT))
        self.ebrect = pygame.Rect((650, y), (BT_WIDTH, BT_HEIGHT))
        self.screen.blit(self.eb, (650, y))

    def about(self):
        self.screen.fill((71, 209, 255))

        self.render_multi_line("Instrukcja", BG_WIDTH/2-100, 50, 40)
        text = """Pojedynczą grę rozgrywa jedna osoba (jeden klient). Klient rozgrywkę rozpoczyna z kontem równym milion złotych. 
Aby wygrać te pieniądze musi odpowiedzieć na 8 pytań. Po każdym pytaniu gracz ma możliwość wyboru 
kategorii pytania spośród dwóch możliwych. Na kategorię składają się tematyczne pytania, 
z puli których zostanie wylosowane jedno pytanie. Na każde z nich ma 60 sekund. Gra odbywa się w okienku 
z czterema polami, które odpowiadają zapadniom. Każdemu z nich przypisana jest jedna możliwa  odpowiedź. 
Gracz wybiera właściwą odpowiedź, podając ilość pieniędzy w wybranym przez siebie  polu. Jeżeli nie są pewny 
odpowiedzi, może rozdzielić pieniądze pomiędzy kilka pól. Po upływie czasu zerowane  są wszystkie pola 
z błędnymi odpowiedziami, w ten sposób zostają na koncie tylko te pieniądze, które zostały przypisane 
na właściwą odpowiedź. Gracz ma możliwość skorzystania z dodatkowych 30 sekund po pytaniu,
podczas których może zmienić rozłożenie pieniędzy na pola ale taką szansę ma tylko raz w czasie całej gry."""
        self.render_multi_line(text, 50, 130, 18)
        self.render_multi_line("Nacisnij [SPACJA],zeby rozpoczac gre",200, BG_HEIGHT-BG_HEIGHT/3,30)

    def render_multi_line(self, text, x, y, rozmiar,color=(255, 255, 0)):
        myfont = pygame.font.SysFont("Arial", rozmiar,bold=True)
        linie = text.splitlines()
        for i, l in enumerate(linie):
            self.screen.blit(myfont.render(l, 1, color), (x, y + rozmiar * i))

    def game(self):
        bg = pygame.image.load('Img/ss.jpg').convert()
        bg = pygame.transform.scale(bg, (BG_WIDTH, BG_HEIGHT))
        self.screen.blit(bg, (0, 0))
        self.start_ticks = pygame.time.get_ticks()

        self.render_multi_line("Pytanie", 20, 20, 45)
        self.render_multi_line("1) odpowiedz", 50, 130, 30)
        self.render_multi_line("2) odpoiwedz", 50, 200, 30)
        self.render_multi_line("3) odpoiwedz", 50, 270, 30)
        self.render_multi_line("4) odpoiwedz", 50, 340, 30)

        settings = {
            "command": self.print_on_enter,
            "inactive_on_enter": False,

        }
        self.entry1 = pygooey.TextBox(rect=(60, 450, 150, 30), **settings, id="1")
        self.entry2 = pygooey.TextBox(rect=(260, 450, 150, 30), **settings, id="2")
        self.entry3 = pygooey.TextBox(rect=(460, 450, 150, 30), **settings, id="3")
        self.entry4 = pygooey.TextBox(rect=(660, 450, 150, 30), **settings, id="4")

        self.zb = pygame.image.load('Img/buttonz.png')
        self.zb = pygame.transform.scale(self.zb, (BT_WIDTH-50, BT_HEIGHT-50))
        self.zbrect = pygame.Rect((10, 520), (BT_WIDTH-50, BT_HEIGHT-50))
        self.screen.blit(self.zb, (10, 520))

    def pytanie(self):
        bg = pygame.image.load('Img/ss.jpg').convert()
        bg = pygame.transform.scale(bg, (BG_WIDTH, BG_HEIGHT))
        self.screen.blit(bg, (0, 0))
        self.client.send_message("Pytanie : "+str(self.iloscPytan))
        self.client.send_message("PYTANIE")
        print('Przed')
        pytanie = self.client.receive_message()
        print('p', pytanie)
        print('1')
        #odp1 = self.client.receive_message()
        #print('odp1', odp1)
        ''' print('2')
        odp2 = self.client.receive_message()
        print('3')
        odp3 = self.client.receive_message()
        print('4')
        odp4 = self.client.receive_message()
        print('Po')'''
        '''self.client.receive_message()
        self.client.receive_message()
        self.client.receive_message()
        self.client.receive_message()
        self.client.receive_message()'''
        print('p',pytanie)
        #print(odp1)
        #print(odp2)
        #print(odp3)

        #pytaniel=pickle.load(pytanie)
        self.render_multi_line(pytanie[0], 20, 20, 35)
        self.render_multi_line('o', 50, 130, 30)
        self.render_multi_line('a', 50, 200, 30)
        self.render_multi_line('x', 50, 270, 30)
        self.render_multi_line('u', 50, 340, 30)
        pygame.display.update()
        self.wait()
        self.game()

    def wait(self):
        start_ticks = pygame.time.get_ticks()
        seconds = round((pygame.time.get_ticks() - start_ticks) / 1000, 0)
        while seconds<15:
            seconds = round((pygame.time.get_ticks() - start_ticks) / 1000, 0)
        return

    def update(self):
        account = self.myfont.render("Stan konta: " + str(self.money) + " ZL", 1, (255, 255, 0))
        self.screen.blit(account, (BG_WIDTH / 2 - 120, 540))

    def updateClock(self, second):
        if self.koniecCzasu ==False:
            if second<=60:
                pygame.display.set_caption('Postaw na milion! Pozostały czas: '+ str(int(60-second))+"s")
            else:
                self.client.send_message("Koniec czasu")
                self.koniecCzasu=True
                self.sprawdza()

    def print_on_enter(self, id, text):
        if text != "":
            self.pole[id]=text

    def sprawdza(self):
        if self.koniecCzasu == True:
            for i in self.pole.keys():
                self.client.send_message("Sprawdzanie odpoiwedzi")
                if(self.prawidlowa==i):
                    self.money=self.pole[i]
                    self.client.send_message("Pozostale pieniadze gracza : "+ str(self.money))
            self.poprawna()

    def poprawna(self):
        self.screen.fill((0, 0, 0))
        self.iloscPytan += 1
        bg = pygame.image.load('Img/ss.jpg').convert()
        bg = pygame.transform.scale(bg, (BG_WIDTH, BG_HEIGHT))
        self.screen.blit(bg, (0, 0))
        self.pole = {str(1): 0, str(2): 0, str(3): 0, str(4): 0}

        self.render_multi_line("Pytanie", 20, 20, 45)
        self.render_multi_line("Poprawna odpowiedz to:", BG_WIDTH/2-100, 150, 45)
        self.render_multi_line("2) odpoiwedz", 50, 200, 30)

        if(self.iloscPytan == 8):
            self.koniec()
        elif(self.money == 0):
            self.koniec()

    def zlicz(self):
        self.postawiono = 0
        for i in self.pole.keys():
            self.postawiono += int(self.pole[i])


    def koniec(self):
        self.screen.fill((0, 0, 0))
        bg = pygame.image.load('Img/ss2.jpg').convert()
        bg = pygame.transform.scale(bg, (BG_WIDTH, BG_HEIGHT))
        self.screen.blit(bg, (0, 0))
        self.render_multi_line("Wygrales : "+str(self.money)+"zl", 20, 20, 45)
        self.client.send_message("Gracz wygral: "+str(self.money))
        self.Game = False
        self.koniecCzasu = False
        y = BG_HEIGHT - BG_HEIGHT / 4
        self.eb = pygame.image.load('Img/buttone.png')
        self.eb = pygame.transform.scale(self.eb, (BT_WIDTH, BT_HEIGHT))
        self.ebrect = pygame.Rect((650, y), (BT_WIDTH, BT_HEIGHT))
        self.screen.blit(self.eb, (650, y))



Game()