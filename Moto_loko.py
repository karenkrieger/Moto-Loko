import sys, os, pygame
import random
from time import time
from pygame.locals import *


def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

WIDTH = 960
HEIGHT = 540

MATRIZ = [['','',''],['','',''],['','',''],['','',''],['','','']]

TARGETFPS = 30

VELOCIDADE = TARGETFPS / 2

frames = 0

allow_spawn = True

carros = []

start_screen = True

game_over = False

score = 0


font = pygame.font.Font(resource_path('assets/fonts/amiga4ever.ttf'),10)

colisionSound = pygame.mixer.Sound(resource_path('assets/sounds/Explosion.wav'))

moveSound = pygame.mixer.Sound(resource_path('assets/sounds/move.wav'))

start_text = font.render('Press start to begin',1,(255,255,255))

gameover_text = font.render("Game Over",1,(255,255,255))


bg = pygame.image.load(resource_path('assets/tiles/bg.jpg')) #background
bg = pygame.transform.scale(bg,(WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Moto Loko')


clock = pygame.time.Clock()

def mapeamento_x(x): # transformar coordenada de matriz em pixels
    return 260 + x * 90

def mapeamento_y(y): # transformar coordenada de matriz em pixels
    return 170 + y * 90

class Moto(object):
    def __init__(self):
        self.image = pygame.image.load(resource_path('assets/tiles/bikepixel.png'))
        self.image = pygame.transform.scale(self.image,(70, 50))
        self.x = 0
        self.y = 1
        
                 
    def draw(self, surface):
        surface.blit(self.image,(mapeamento_x(self.x), mapeamento_y(self.y)))

    def hit (self):
        self.image = pygame.image.load(resource_path('assets/tiles/oie_1533958s1Pl3jJS.png'))
        self.image = pygame.transform.scale(self.image,(70, 50))
        colisionSound.play()
        self.draw(screen)

class Carro(object):
    def __init__(self,x,y):
        self.image = pygame.image.load(resource_path('assets/tiles/carpixel.png'))
        self.image = pygame.transform.scale(self.image, (90, 50)) #Carro ocupa 5 posições na tela
        self.x = x
        self.y = y
        self.remove = False
        MATRIZ[self.x][self.y] = 'X'
        
    def draw(self, surface):
        surface.blit(self.image, (mapeamento_x(self.x), mapeamento_y(self.y)))

    def move(self):
        global score
        self.x = self.x - 1
        MATRIZ[self.x+1][self.y] = ''
        if self.x < 0:
            self.remove = True
            score += 1
        else:
            MATRIZ[self.x][self.y] = 'X'
        
        
moto = Moto()

def spawn():
        carros.append(Carro(4,random.randint(0,2)))

def colision():
    global game_over
    if MATRIZ[moto.x][moto.y] == 'X':
        game_over = True
        moto.hit()
        screen.blit(gameover_text,(260, 130))
        
def game_reset():
    global score
    global frames
    frames = 0
    score = 0
    while len(carros) > 0:
        carros.remove(carros[0])
    for x in range(len(MATRIZ)):
        for y in range(len(MATRIZ[x])):
            MATRIZ[x][y] = ''
    moto.y = 1

while start_screen == True: #tela inicial
    screen.blit(bg,(0,0))
    moto.draw(screen)
    screen.blit(start_text,(480, 130))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start_screen = False
            if event.key == pygame.K_ESCAPE:
                pygame.quit() ; sys.exit(0)
        if event.type == pygame.QUIT:
            pygame.quit() ; sys.exit(0)

while True: #main loop
    
    if game_over == False: #loop de jogo
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and moto.y < 2:
                    moto.y += 1
                    moveSound.play()
                if event.key == pygame.K_UP and moto.y > 0:
                    moto.y -= 1
                    moveSound.play()
            if event.type == pygame.QUIT:
                    pygame.quit() ; sys.exit(0)

        screen.blit(bg,(0,0))

        score_display = font.render('Score: ' + str(score),1,(255,255,255))
        screen.blit(score_display,(500, 130))

        moto.draw(screen)
        for c in carros:
            c.draw(screen)

        colision()

        if frames != 0 and frames%VELOCIDADE == 0:
            frames = 0

            if len(carros) > 0:
                for c in carros:
                    c.move()
                for c in carros:
                    if c.remove == True:
                        carros.remove(c)

            if allow_spawn == True:
                spawn()
            
            allow_spawn = not allow_spawn

        frames += 1

        pygame.display.update()
        clock.tick(TARGETFPS)
        
    else: #tela de game over
        while game_over == True:
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = False
                        moto = Moto()
                        game_reset()
                    if event.key == pygame.K_ESCAPE:
                         pygame.quit() ; sys.exit(0)
                if event.type == pygame.QUIT:
                    pygame.quit() ; sys.exit(0)

pygame.quit()
