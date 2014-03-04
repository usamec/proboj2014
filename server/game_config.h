#ifndef GAME_CONFIG_H__
#define GAME_CONFIG_H__
#include "player1.h"
#include "player2.h"
static int n_players = 2;
inline Unit* CreatePlayerUnit(int id) {
  if (id == 1) return new Player1();
  if (id == 2) return new Player2();
}
#endif
