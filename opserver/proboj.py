import random, pygame, sys
import json
import pprint
import numpy as np
from pygame.locals import *

FPS = 2
WINDOWWIDTH = 1000
WINDOWHEIGHT = 600

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 200,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)

BGCOLOR = WHITE

mapa = []
steps = []
cukor = []
state = 0

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    global mapa, steps, cukor
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Cukor')

    
    while True:
        getInput()
        runGame()
        showStats()

def getInput():
    
    global mapa, steps, cukor
    
    raw = raw_input()
    print "WANA BANANA?"
    funnyStruct = json.loads(raw)
    #pprint.pprint(funnyStruct)
    
    print "!!!!!!load finished with pro problem"
        
    mapa = funnyStruct['map']
    steps = funnyStruct['steps']
    cukor = [ [0 for i in range(mapa['c'])] for j in range(mapa['r']) ]
    
    
    #pprint.pprint(mapa)
    #pprint.pprint(environment)

def runGame():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    global mapa, steps, cukor
    
    
    print "Game is running"
    print "mapa"
    pprint.pprint (mapa)
    print "kroky"
    pprint.pprint (steps)
    print "cukor"
    pprint.pprint (cukor)
    
    
    wanaHelp = False
    
    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_h):
                    print "lol"
                    wanaHelp = not wanaHelp
                
                elif event.key == K_ESCAPE:
                    terminate()

        
        DISPLAYSURF.fill(BGCOLOR)
        
        drawMap()
        
        gameUpdate()
        
        if wanaHelp :
            drawHelp()
        
        pygame.display.update()
        
        
        
        FPSCLOCK.tick(FPS)

        
def gameUpdate():
    global mapa, steps, cukor, state
    
    dejeSa = steps[state]   
    state= state+1
    
    for c in dejeSa['zucker']:
        cukor[c['y']][c['x']] = c['new_ammount']


def drawMap():
    global mapa, steps, cukor
    
    iHaveX, iHavey = 600, 600
    velkost = computeSize()
    velkost = 20
    
    marginTop, marginLeft = 10, 10
    
    for i in range(mapa['r']):
        for j in range(mapa['c']):
            policko = pygame.Rect(marginLeft + j*velkost, marginTop + i*velkost, marginLeft + (j+1)*velkost, marginTop + (i+1)*velkost)
            pygame.draw.rect(DISPLAYSURF, getColor(mapa['data'][i][j],cukor[i][j]) , policko)


def getColor(coJe, cukor):
    if coJe != 0:
        return BLACK
    else: 
        return (cukor*20, 200+ cukor*5, cukor*20)


def computeSize():
    return 0
    

def drawHelp():
    helpSurf = BASICFONT.render('Score: %s', True, BLACK) #funky options
    helpRect = helpSurf.get_rect()
    helpRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(helpSurf, helpRect)
    
def terminate():
    pygame.quit()
    sys.exit()

def showStats():
    pass

if __name__ == '__main__':
    main()