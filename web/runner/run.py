import os
import datetime
import random
import sys

n_players = 4
cur_scores = [0 for x in xrange(n_players)]
if os.path.exists("../logs/scores.txt"):
  f = open("../logs/scores.txt")
  cur_scores = [int(x) for x in f]
  assert(len(cur_scores) == n_players)
  f.close()

cmd = "python compile_game.py all ";
for x in xrange(n_players):
  cmd += "../players/%d.au " % x

print cmd
if not os.system(cmd) == 0:
  print "compile failed"
  sys.exit(1)

filename = datetime.datetime.now().strftime("../logs/%Y_%m_%d_%H_%M_%S.log")

ma = "../maps/" + random.choice(os.listdir("../maps/"))

print ma

cmd2 = "./server %s %s" % (ma, filename)

os.system(cmd2)

f = open(filename+".scr")
cs = [int(x) for x in f]
assert(len(cs) == n_players)
f.close()

for i in xrange(n_players):
  cur_scores[i] += cs[i]

f = open("../logs/scores.txt", "w")
for x in cur_scores:
  print >>f, x

f.close()
