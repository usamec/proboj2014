#ifndef GAME_CONFIG_H__
#define GAME_CONFIG_H__

static int n_players = 2;

inline Unit* CreatePlayerUnit(int id) {
  return new Unit();
}

#endif
