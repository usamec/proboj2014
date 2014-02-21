#ifndef GAME_CONFIG_H__
#define GAME_CONFIG_H__

#include "player1.h"

static int n_players = 2;

inline Unit* CreatePlayerUnit(int id) {
  return new Player1();
}

#endif
