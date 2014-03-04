import sys
import os

def usage():
  print """Usage:
all HRAC_1 HRAC_2 ...
precompile HRAC_1 HRAC_2 ...
compile"""
  sys.exit()

if len(sys.argv) < 2:
  usage()

def precompile(players):
  if len(players) < 1:
    usage()

  for i, x in enumerate(players):
    os.system("python compile_player.py %s %d >player%d.h" % (x, i+1, i+1))

  f = open("game_config.h", "w")
  print >>f, "#ifndef GAME_CONFIG_H__"
  print >>f, "#define GAME_CONFIG_H__"

  for i in xrange(len(players)):
    print >>f, '#include "player%d.h"' % (i+1)

  print >>f, "static int n_players = %d;" % (len(players))
  print >>f, "inline Unit* CreatePlayerUnit(int id) {"
  for i in xrange(len(players)):
    print >> f, "  if (id == %d) return new Player%d();" % (i+1, i+1)
  print >> f, "}"
  print >>f, "#endif"
  f.close()


def compile():
  os.system("g++ -O2 server.cc -std=gnu++0x -o server")

if sys.argv[1] == 'all':
  precompile(sys.argv[2:])
  compile()

elif sys.argv[1] == 'compile':
  compile()

elif sys.argv[1] == 'precompile':
  precompile(sys.argv[2:])

else:
  usage()
