import random as ran
import pprint

p = 4
minSiz,maxSiz = 10, 25

ran.seed()
c,u = ran.randint(minSiz,maxSiz),ran.randint(3,15)
r=c
wall = r*c/10
cukor= r*c/50
stvor= int(c**(0.5))
stvor+=1
print str(r)+' '+str(c)+' '+str(u)

mapa=  [[0 for i in xrange(c)] for j in xrange(r)]

for i in xrange(cukor):
    kolko = ran.randint(0,10)
    kamC = ran.randint(0,c-1)
    kamR = ran.randint(0,r-1)
    if mapa[kamR][kamC]==0:
        mapa[kamR][kamC]=0.0

    if kolko>8:
        mapa[kamR][kamC]+=0.1
    else: mapa[kamR][kamC]+=0.01


for i in xrange(wall):
    kamC = ran.randint(0,c-1)
    kamR = ran.randint(0,r-1)
    mapa[kamR][kamC]= -1

    
for i in xrange(stvor):
    mapa[i][0:stvor] = [1 for j in xrange(stvor)]
    mapa[-i-1][0:stvor] = [2 for j in xrange(stvor)]
    mapa[i][0-stvor+1:] = [3 for j in xrange(stvor)]
    mapa[0-1-i][0-stvor+1:] = [4 for j in xrange(stvor)]
    


for rr in mapa:
    for cc in rr:
        print cc,
    print ""
