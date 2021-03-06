#done : test na velke mapy, 
#todo: farebne mravce, staty na konci, zoom na miesto, sledovanie hraca, zuckerbar, go back

import random, pygame, sys
import json
import pprint
import numpy as np
from pygame.locals import *
import os

names = ["Japonsko", "Mexiko", "Rusko", "Taliansko"]
FPS = 500
skipin = 10
skiped = 0
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
pooop = []
state = 0
dejeSa = []
velkost = 10
stav = "running"
args = sys.argv[1:]
mypath = os.path.dirname(os.path.abspath(__file__))
hracc0 = pygame.image.load(mypath + '/japonskoicon.png')
hovienko = pygame.image.load(mypath + '/poooooop.gif')

#hracc0 = pygame.transform.scale(hracc0,(velkost,velkost))
marginTop, marginLeft = 20, 20
counter = 0

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    global mapa, steps, cukor, skipin, skiped
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Cukor')
    
    getInput()
    pygame.display.toggle_fullscreen()
    runGame()
    showStats()
    pass

def getInput():
    
    global mapa, steps, cukor, hracc0, velkost, hovienko, pooop
    raw = ""
    
    
    if len(sys.argv)>1:
        path = sys.argv[1]
        if os.path.exists(path):
            raw = open(path,'r').read()
        else: print "invalid file"
    else: raw = raw_input()
    
    print "WANA BANANA?"
    
    funnyStruct = json.loads(raw)
    #pprint.pprint(funnyStruct)
    
    print "!!!!!!load finished with pro problem"
        
    mapa = funnyStruct['map']
    
    #mapa = {'c':100, 'r':100, 'data': [[0 for j in range(100)] for i in range(100)]}
    #mapa = {'c':10, 'r':10, 'data': [[0 for j in range(10)] for i in range(10)]}
    
    steps = funnyStruct['steps']
    cukor = [ [0 for i in range(mapa['c'])] for j in range(mapa['r']) ]
    pooop = [ [0 for i in range(mapa['c'])] for j in range(mapa['r']) ]
    
    velkost = min(600/mapa['r'],600/mapa['c'])
    hracc0 = pygame.transform.scale(hracc0,(velkost-2,velkost-2))       
    hovienko = pygame.transform.scale(hovienko,(max(5,velkost/2),max(5,velkost/2)))       
    #hovienko = hovienko.set_alpha(10)
    #pprint.pprint(mapa)
    #pprint.pprint(environment)
    pass

def runGame():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, FPS, counter
    global mapa, steps, cukor, stav, skipin, skiped, dejeSa, state
    
    
    print "Game is running"
    print "mapa"
    #pprint.pprint (mapa)
    print "kroky"
    #pprint.pprint (steps)
    print "cukor"
    #pprint.pprint (cukor)
    
    
    wanaHelp = False
    
    while True: # main game loop
        if stav== "running":
            counter+=1
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                
                
                if event.key == K_ESCAPE:
                    terminate()
                elif '-c' in args:
                    continue
                
                elif (event.key == K_h):
                    print "help"
                    wanaHelp = not wanaHelp
                
                elif event.key == K_s:
                    if stav == "running":
                        stav = "paused"
                    else:
                        stav = "running"

                elif event.key == K_f:
                    pygame.display.toggle_fullscreen()
                elif event.key == K_q:
                    FPS-=1
                    if FPS <= 1:
                        FPS = 1
                elif event.key == K_w:
                    FPS += 1
                elif event.key == K_t:
                    skipin += 1
                elif event.key == K_y:
                    skipin = max(0,skipin-1)
                
                elif event.key == K_e:
                    FPS -= 10
                    FPS = max(1,FPS)
                elif event.key == K_r:
                    FPS += 10
                    
                    
        if stav == "running":
            gameUpdate()
        
	if skiped>=skipin or len(steps[state]['attacks'])>0:
		
        	DISPLAYSURF.fill(BGCOLOR)
                skiped=0
		drawMap()
		drawPoop()
		drawPlayers()
		drawMsg()
		drawFight()
		drawScore()
		drawTotalScores()        
	        pygame.display.update()
        
        else: skiped+=1

        if wanaHelp :
            drawHelp()
        
        
        
        if stav == 'end':
            return
        FPSCLOCK.tick(FPS)
    pass

def drawTotalScores():
  
  mypath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  if os.path.exists(mypath+"/web/logs/scores.txt"):
    f = open(mypath+"/web/logs/scores.txt")
    scores = [x.strip() for x in f]
    f.close()
    scoreSurf = BASICFONT.render("Celkove skore:", True, BLACK) #funky options
    scoreRect = scoreSurf.get_rect()
    scoreRect.topright = (WINDOWWIDTH - 20, 420)
    DISPLAYSURF.blit(scoreSurf, scoreRect)   
    for i,s in enumerate (scores):
      scoreSurf = BASICFONT.render(names[i]+ ': ' + str(s), True, getPlayerColor(i)) #funky options
      scoreRect = scoreSurf.get_rect()
      scoreRect.topright = (WINDOWWIDTH - 20, 400+20*(i+2))
      DISPLAYSURF.blit(scoreSurf, scoreRect)
  else:
    #assert(False)
    pass

def gameUpdate():
    global mapa, steps, cukor, state, dejeSa, stav
    
    dejeSa = steps[state]   
    state= state+1
    if state >= len(steps)-1:
        stav= "end"
        return
        
        
    for p in dejeSa['writes']:
        pooop[p['y']][p['x']] = 1000    
    for c in dejeSa['zucker']:
        cukor[c['y']][c['x']] = c['new_ammount']
    #print "cas:",
    #print (counter)
    #print ("dejesa: ")
    #pprint.pprint(dejeSa)
    

def iWanaRect(x, y, size):
    global mapa, velkost
    
    iHaveX, iHaveY = 600, 600
    velkost = (min(iHaveX / mapa['r'] , iHaveY / mapa['c']))
    
    return pygame.Rect(marginLeft + x*velkost - size, marginTop + y*velkost - size, velkost + size*2, velkost + size*2)

def iWanaPoz(x,y,sizex,sizey):
    """vrati pixelovu poziciu hraca na gride"""
    
    return (marginLeft + x*velkost - sizex/2 + velkost/2, marginTop + y*velkost - sizey/2 + velkost/2)
    pass

def drawPoop():
    
    global mapa, steps, cukor, velkost
        
    for i in range(mapa['r']):
        for j in range(mapa['c']):
            if pooop[i][j]==0:
                continue
            pooop[i][j]-=1
            DISPLAYSURF.blit(hovienko, iWanaRect(j-1,i,0).topright)
                
    pass


def drawMap():
    global mapa, steps, cukor, velkost
        
    for i in range(mapa['r']):
        for j in range(mapa['c']):
            policko = iWanaRect(j,i,0)
            pygame.draw.rect(DISPLAYSURF, getColor(mapa['data'][i][j],cukor[i][j]) , policko)
            if mapa['bases'][i][j]>0 and mapa['bases'][i][j]<6:
                policko = iWanaRect(j,i,0)
                pygame.draw.rect(DISPLAYSURF,  getBaseColor(mapa['bases'][i][j]-1) , policko)
            
    pass

def drawPlayers():
    """nakresli hraca a zuckerbar"""
    global dejeSa, velkost
    
    for i, player in enumerate (dejeSa['units']):
        
        for minion in player:
            char = iWanaRect(1,1,0)
            if i == 0:    
                
                DISPLAYSURF.blit(hracc0, iWanaRect(minion['x']-1,minion['y'],0).topright)
                char = iWanaRect(minion['x'],minion['y'],0)
 
            else:
                char = iWanaRect(minion['x'],minion['y'],-2)
                pygame.draw.rect(DISPLAYSURF, getPlayerColor(i) , char)
            #DISPLAYSURF.blit(hracc, iWanaPoz(minion['x'],minion['y'], 20,30))

            cukerBar = iWanaRect(minion['x'],minion['y'],0)
            cukerBar.height = 3
            cukerBar.width = float(minion['carry']*velkost)/10
            cukerBar.center = char.center
            cukerBar.bottom = char.top+2-4
            
            if minion['carry']>0:
                pygame.draw.rect(DISPLAYSURF, WHITE , cukerBar)
            
    pass
    
    
def drawFight():
    """kresli boje"""
    global velkost, dejeSa,steps;
    if state >= len(steps): 
        return
    nex = steps[state] 
    
    for i,msg in enumerate(nex['attacks']):
        plF = dejeSa['units'][msg['from_player']-1]
        plT = dejeSa['units'][msg['to_player']-1]
        
        fro = plF[msg['from_id']-1]
        to = plT[msg['to_id']-1]
        
        war = iWanaRect(float(fro['x']+to['x']) /2 ,float(fro['y']+to['y'])/2, (float (0-velkost)) /4)
        pygame.draw.rect(DISPLAYSURF, RED , war)
        
        if msg['success']==1:
            #zomri druheho
            kil = iWanaRect(to['x'],to['y'],0-2)
            pygame.draw.rect(DISPLAYSURF, RED, kil)
            """
            fightKill = BASICFONT.render('p: '+ str(msg['from_player']) , True, getPlayerColor(msg['from_player']-1)) 
            fightRect = fightKill.get_rect()
            fightRect.topright = (20+(i+1)*150, 600+20)
            DISPLAYSURF.blit(fightKill, fightRect)
            
            fightKill = BASICFONT.render(' vyhral proti ', True, BLACK) 
            fightRect = fightKill.get_rect()
            fightRect.topleft = (20+(i+1)*150, 600+20)
            DISPLAYSURF.blit(fightKill, fightRect)
            
            
            fightKill = BASICFONT.render('p '+ str(msg['to_player']) , True, getPlayerColor(msg['to_player']-1)) 
            fightRect = fightKill.get_rect()
            fightRect.topleft = (100+(i+1)*150, 600+20)
            DISPLAYSURF.blit(fightKill, fightRect)
            """
        
    pass

def drawMsg():
    global dejeSa, velkost
    
    
    
    for msg in dejeSa['msgs']:
        pl = dejeSa['units'][msg['player_id']-1]
        fro = pl[msg['from']-1]
        to = pl[msg['to']-1]
        
        
        pygame.draw.line(DISPLAYSURF, BLUE, iWanaPoz(fro['x'],fro['y'],0,0), iWanaPoz(to['x'],to['y'],0,0), 2)
        
    pass

    
def getColor(coJe, cukor):
    
    if coJe != 0:
        return BLACK
    else: 
        return (cukor*25, 200+ cukor*5, cukor*25)

def bright(color,x):
    return tuple(max(0,min(255,x+q) ) for q in color)
    


def getPlayerColor(kto):
    """ vrati farbu hraca"""
    if kto == 1:
        return ( 160, 84, 47) #mexico
    elif kto == 2:
        return (0, 0, 200) # rusko
    elif kto == 3:
        return (200, 0, 200) # taliansko
    elif kto == 4:
        return (255, 128 , 0)
    elif kto == 5:
        return (0, 0, 0)
    elif kto == 0:
        return (255,100,100) # japonsko
    else: return (50,50,50)    

def getBaseColor(kto):
    """ vrati farbu hraca"""
    const = 60
    pom = getPlayerColor(kto)
    
    return bright(pom,const)

def drawScore():
    global dejeSa, FPS, FPSCLOCK
    
    scoreSurf = BASICFONT.render('FPS: '+ str(FPS)+" "+("%.1f"%FPSCLOCK.get_fps())+ '  frame: ' + str(counter), True, BLACK) #funky options
    scoreRect = scoreSurf.get_rect()
    scoreRect.topright = (WINDOWWIDTH - 20, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
        
    for i,s in enumerate (dejeSa['scores']):
        scoreSurf = BASICFONT.render(names[i]+ ': ' + str(dejeSa['scores'][i]), True, getPlayerColor(i)) #funky options
        scoreRect = scoreSurf.get_rect()
        scoreRect.topright = (WINDOWWIDTH - 20, 20*(i+2))
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
