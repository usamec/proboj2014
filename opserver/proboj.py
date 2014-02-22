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
dejeSa = []
velkost = 0
stav = "running"



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
    global mapa, steps, cukor, stav
    
    
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
                
                elif event.key == K_s:
                    if stav == "running":
                        stav = "paused"
                    else:
                        stav = "running"

                elif event.key == K_ESCAPE:
                    terminate()

        
        DISPLAYSURF.fill(BGCOLOR)
        if stav == "running":
            gameUpdate()
        
        drawMap()
        drawPlayers()
        
        
        
        if wanaHelp :
            drawHelp()
        
        pygame.display.update()
        
        
        
        FPSCLOCK.tick(FPS)


def gameUpdate():
    global mapa, steps, cukor, state, dejeSa
    
    dejeSa = steps[state]   
    state= state+1
    if state > len(steps):
        state= "end"
        return
        
    for c in dejeSa['zucker']:
        cukor[c['y']][c['x']] = c['new_ammount']
    
    pprint.pprint(dejeSa)
    pprint.pprint(cukor)

def iWanaRect(x, y, size):
    global mapa, velkost
    
    iHaveX, iHavey = 300, 300
    velkost = (min(iHaveX / mapa['c'] , iHavey / mapa['r']))
    
    
    marginTop, marginLeft = 20, 20
    
    return pygame.Rect(marginLeft + x*velkost - size, marginTop + y*velkost - size, velkost + size, velkost + size)
            

def drawMap():
    global mapa, steps, cukor, velkost
        
    for i in range(mapa['r']):
        for j in range(mapa['c']):
            policko = iWanaRect(j,i,0)
            pygame.draw.rect(DISPLAYSURF, getColor(mapa['data'][i][j],cukor[i][j]) , policko)

def drawPlayers():
    global dejeSa
    
    for i, player in enumerate (dejeSa['units']):
        for minion in player:
            character = iWanaRect(minion['x'],minion['y'],2)
            pygame.draw.rect(DISPLAYSURF, (100*i,150, 150) , character)


def getColor(coJe, cukor):
    if coJe != 0:
        return BLACK
    else: 
        return (cukor*20, 200+ cukor*5, cukor*20)


def drawHelp():
    helpSurf = BASICFONT.render('s- stop, Esc - koniec, ', True, BLACK) #funky options
    helpRect = helpSurf.get_rect()
    helpRect.topleft = (WINDOWWIDTH - 200, 10)
    DISPLAYSURF.blit(helpSurf, helpRect)
    
def terminate():
    pygame.quit()
    sys.exit()

def showStats():
    pass

if __name__ == '__main__':
    main()