#include "map.h"
#include "game_config.h"
#include <cstdio>

void GetEmptyPos(Game &g, int team, int &y, int &x) {
  for (int i = 0; i < g.g.size(); i++) {
    for (int j = 0; j < g.g[i].size(); j++) {
      if (g.g[i][j].base == team) {
        bool occ = false;
        for (int k = 0; k < g.units.size(); k++) {
          if (g.units[k]->y == i && g.units[k]->x == j) {
            occ = true;
            break;
          }
        }
        if (!occ) {
          y = i;
          x = j;
          return;
        }
      }
    }
  }
}

Game LoadGame(char* fn) {
  FILE *f = fopen(fn, "r");
  Game g;
  int r, c;
  fscanf(f, "%d %d %d", &r, &c, &g.units_per_team);
  g.g.resize(r, vector<Point>(c));
  for (int i = 0; i < r; i++) {
    for (int j = 0; j < c; j++) {
      double x; fscanf(f, "%lf", &x);
      if (x < 0) {
        g.g[i][j].wall = true;
      } else if (x >= 1) {
        g.g[i][j].base = (int)(x-1);
      }
      else g.g[i][j].zucker_prob = x;
    }
  }
  for (int i = 0; i < n_players; i++) {
    for (int j = 0; j < g.units_per_team; j++) {
      int x, y;
      GetEmptyPos(g, i, y, x);
      Unit* u = CreatePlayerUnit(i);
      u->y = y;
      u->x = x;
      g.units.push_back(u);
    }
  }

  return g;
};

int main(int argc, char** argv) {
  Game g = LoadGame(argv[1]);
  printf("init done\n");
}
