#include "map.h"
#include "game_config.h"
#include <cstdio>
#include <algorithm>
#include <unordered_map>

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
      u->id = j;
      u->g = &g;
      u->player_id = i;
      g.units.push_back(u);
    }
  }

  return g;
};

void Unit::Step() {
  // TODO: inbox
  // TODO: area
  // TODO: Basic vars
  data["X"] = x;
  data["Y"] = y;
  moved = false;
  RealStep();
}

void Unit::MOVE(int yy, int xx) {
  if (moved) return;
  moved = true;
  yy = max(-1, min(1, yy));
  xx = max(-1, min(1, xx));
  int px = x;
  int py = y;
  x += xx;
  y += yy;
  x = max(0, min((int)g->g[0].size()-1, x));
  y = max(0, min((int)g->g.size()-1, y));
  if (g->g[y][x].wall == true) {
    x = px;
    y = py;
  }
}

void LogMap(FILE *flog, Game &g) {
  fprintf(flog, "\"map\":{\"r\": %d, \"c\": %d, \"data\":[", g.g.size(), g.g[0].size());
  for (int i = 0; i < g.g.size(); i++) {
    fprintf(flog, "[");
    for (int j = 0; j < g.g[i].size(); j++) {
      fprintf(flog, "%d%c", g.g[i][j].wall ? 1 : 0, j + 1 == g.g[i].size() ? ']' : ',');
    }
    fprintf(flog, "%c", i + 1 == g.g.size() ? ']' : ',');
  }
  fprintf(flog, "}");
}

int main(int argc, char** argv) {
  Game g = LoadGame(argv[1]);
  FILE* flog = fopen(argv[2], "w");
  fprintf(flog, "{");
  LogMap(flog, g);
  printf("init done\n");

  fprintf(flog, ", \"steps\": [");
  int n_steps = 3;
  for (int st = 0; st < n_steps; st++) {
    // TODO: randomize steps
    // TODO: zucker
    // TODO: scores
    printf("ss %d %d\n", g.units[st%g.units.size()]->y,
           g.units[st%g.units.size()]->x);
    g.units[st%g.units.size()]->Step();
    printf("ee %d %d\n", g.units[st%g.units.size()]->y,
           g.units[st%g.units.size()]->x);

    // Logging
    fprintf(flog, "{\"units\": [");
    for (int i = 0; i < n_players; i++) {
      fprintf(flog, "[");
      for (int j = 0; j < g.units_per_team; j++) {
        fprintf(flog, "{\"y\": %d, \"x\": %d}%c", g.units[i*g.units_per_team+j]->y,
                g.units[i*g.units_per_team+j]->x, j + 1 == g.units_per_team ? ']' : ',');
      }
      fprintf(flog, "%c", i + 1 == n_players ? ']' : ',');
    }
    fprintf(flog, "}%c", st + 1 == n_steps ? ']' : ','); 
  }
  fprintf(flog, "}");

  fclose(flog);
}
