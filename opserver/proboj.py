#done : test na velke mapy, 
#todo: farebne mravce, staty na konci, zoom na miesto, sledovanie hraca, zuckerbar, go back

import random, pygame, sys
import json
import pprint
import numpy as np
from pygame.locals import *

FPS = 2
WINDOWWIDTH = 1000
WINDOWHEIGHT = 700

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 200,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BLUE      = (100, 100, 200)
BGCOLOR = WHITE

mapa = []
steps = []
cukor = []
state = 0
dejeSa = []
velkost = 0
stav = "running"
hracc = pygame.image.load('opserver/mravec-7.png')
hracc = pygame.transform.scale(hracc,(15,20))


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
    pass

def getInput():
    
    global mapa, steps, cukor
    
    raw = raw_input()
    print "WANA BANANA?"
    funnyStruct = json.loads(raw)
    #pprint.pprint(funnyStruct)
    
    print "!!!!!!load finished with pro problem"
        
    mapa = funnyStruct['map']
    
    #mapa = {'c':100, 'r':100, 'data': [[0 for j in range(100)] for i in range(100)]}
    #mapa = {'c':10, 'r':10, 'data': [[0 for j in range(10)] for i in range(10)]}
    
    steps = funnyStruct['steps']
    cukor = [ [0 for i in range(mapa['c'])] for j in range(mapa['r']) ]
    
    
    #pprint.pprint(mapa)
    #pprint.pprint(environment)
    pass

def runGame():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, FPS
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
                    print "help"
                    wanaHelp = not wanaHelp
                
                elif event.key == K_s:
                    if stav == "running":
                        stav = "paused"
                    else:
                        stav = "running"

                elif event.key == K_ESCAPE:
                    terminate()
                
                elif event.key == K_q:
                    FPS-=1
                    if FPS <= 1:
                        FPS = 1
                elif event.key == K_w:
                    FPS += 1
                    
        DISPLAYSURF.fill(BGCOLOR)
        if stav == "running":
            gameUpdate()
        
        drawMap()
        drawPlayers()
        drawMsg()
        drawScore()        
        
        if wanaHelp :
            drawHelp()
        
        pygame.display.update()
        
        
        if stav == 'end':
            return
        FPSCLOCK.tick(FPS)
    pass


def gameUpdate():
    global mapa, steps, cukor, state, dejeSa, stav
    
    dejeSa = steps[state]   
    state= state+1
    if state >= len(steps)-1:
        stav= "end"
        return
        
    for c in dejeSa['zucker']:
        cukor[c['y']][c['x']] = c['new_ammount']
    
    pprint.pprint(dejeSa)
    pprint.pprint(cukor)


def iWanaRect(x, y, size):
    global mapa, velkost
    
    iHaveX, iHavey = 600, 600
    velkost = (min(iHaveX / mapa['c'] , iHavey / mapa['r']))
    
    
    marginTop, marginLeft = 20, 20
    
    return pygame.Rect(marginLeft + x*velkost - size, marginTop + y*velkost - size, velkost + size*2, velkost + size*2)



def drawMap():
    global mapa, steps, cukor, velkost
        
    for i in range(mapa['r']):
        for j in range(mapa['c']):
            policko = iWanaRect(j,i,0)
            pygame.draw.rect(DISPLAYSURF, getColor(mapa['data'][i][j],cukor[i][j]) , policko)
    pass

def drawPlayers():
    global dejeSa, velkost
    
    for i, player in enumerate (dejeSa['units']):
        for minion in player:
            character = iWanaRect(minion['x'],minion['y'],2)
            pygame.draw.rect(DISPLAYSURF, getPlayerColor(i) , character)
            DISPLAYSURF.blit(hracc, (20+minion['x']*velkost + velkost/2 - 10, 20+minion['y']*velkost + velkost/2 - 15) )
    pass

def drawMsg():
    global dejeSa, velkost
    
    for msg in dejeSa['msgs']:
        pl = dejeSa['units'][msg['player_id']-1]
        fro = pl[msg['from']-1]
        to = pl[msg['to']-1]
        
        
        pygame.draw.line(DISPLAYSURF, BLUE, (fro['x']*velkost+20+ velkost/2, fro['y']*velkost+20+ velkost/2), (to['x']*velkost+20+ velkost/2, to['y']*velkost+20+ velkost/2), 2)
        
    pass

    
def getColor(coJe, cukor):
    if coJe != 0:
        return BLACK
    else: 
        return (cukor*20, 200+ cukor*5, cukor*20)

def getPlayerColor(kto):
    return (100*kto,150, 100*kto)


def drawScore():
    global dejeSa, FPS
    for i,s in enumerate (dejeSa['scores']):
        scoreSurf = BASICFONT.render('player '+ str(i+1)+ ': ' + str(dejeSa['scores'][i]), True, getPlayerColor(i)) #funky options
        scoreRect = scoreSurf.get_rect()
        scoreRect.topright = (WINDOWWIDTH - 20, 20*(i+1))
        DISPLAYSURF.blit(scoreSurf, scoreRect)
    pass
    

def drawHelp():
    helpSurf = BASICFONT.render('s- stop, Esc - koniec', True, BLACK) #funky options
    helpRect = helpSurf.get_rect()
    helpRect.topright = (WINDOWWIDTH - 30, 10)
    DISPLAYSURF.blit(helpSurf, helpRect)
    
def terminate():
    pygame.quit()
    sys.exit()

def showStats():
    pass

if __name__ == '__main__':
    main()
