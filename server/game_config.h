#ifndef GAME_CONFIG_H__
#define GAME_CONFIG_H__
#include "player1.h"
static int n_players = 1;
inline Unit* CreatePlayerUnit(int id) {
  if (id == 1) return new Player1();
}
#endif
