#ifndef GAME_CONFIG_H__
#define GAME_CONFIG_H__
#include "player1.h"
#include "player2.h"
#include "player3.h"
#include "player4.h"
static int n_players = 4;
inline Unit* CreatePlayerUnit(int id) {
  if (id == 1) return new Player1();
  if (id == 2) return new Player2();
  if (id == 3) return new Player3();
  if (id == 4) return new Player4();
}
#endif
