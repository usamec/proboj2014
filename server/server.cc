#include "map.h"
#include "game_config.h"
#include <cstdio>
#include <algorithm>
#include <unordered_map>

vector<int> scores;

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
  scores.resize(n_players);
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
      g.g[i][j].marks.resize(n_players);
    }
  }
  for (int i = 0; i < n_players; i++) {
    for (int j = 0; j < g.units_per_team; j++) {
      int x, y;
      GetEmptyPos(g, i, y, x);
      Unit* u = CreatePlayerUnit(i);
      u->y = y;
      u->x = x;
      u->id = j+1;
      u->g = &g;
      u->player_id = i+1;
      g.units.push_back(u);
    }
  }

  return g;
};

void Unit::MSG(int unit_id, vector<int> msg) {
  for (int i = 0; i < g->units.size(); i++) {
    if (g->units[i]->player_id == player_id && g->units[i]->id == unit_id) {
      g->cur_msgs.push_back(make_pair(player_id, make_pair(id, unit_id)));
      g->units[i]->inbox.clear();
      g->units[i]->inbox[0] = msg.size();
      for (int j = 0; j < msg.size(); j++) {
        g->units[i]->inbox[j+1] = msg[j];
      }
    }
  }
}

void Unit::Step() {
  // TODO: inbox
  data["X"] = x;
  data["Y"] = y;
  data["PL_ID"] = player_id;
  data["ID"] = id;
  data["MAX_ID"] = g->units_per_team;
  data["CARRY"] = carry;
  moved = false;
  putted = false;
  grabbed = false;
  written = false;
  AREA_PL.clear();
  AREA_BASE.clear();
  AREA_WALL.clear();
  AREA_ZUCK.clear();
  AREA_MARKS.clear();
  int sur = 2;
  for (int i = -sur; i <= sur; i++) {
    for (int j = -sur; j <= sur; j++) {
      if (abs(i) + abs(j) > sur) continue;
      int ry = y - i;
      int rx = x - j;
      if (ry < 0 || rx < 0 || ry >= g->g.size() || rx >= g->g[0].size()) continue;
      AREA_PL[i][j] = 0;
      for (int k = 0; k < g->units.size(); k++) {
        if (g->units[k]->x == rx && g->units[k]->y == ry) {
          if (g->units[k]->player_id != player_id) 
            AREA_PL[i][j] = g->units[k]->player_id; 
          else
            AREA_PL[i][j] = -g->units[k]->id;
        }
      }

      AREA_BASE[i][j] = g->g[ry][rx].base+1;
      AREA_WALL[i][j] = g->g[ry][rx].wall;
      AREA_ZUCK[i][j] = g->g[ry][rx].zucker;
      AREA_MARKS[i][j] = g->g[ry][rx].marks[player_id-1];
    }
  }
  RealStep();
  inbox.clear();
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
  // TODO: check other units
  if (g->g[y][x].wall == true) {
    x = px;
    y = py;
  }
}

void Unit::WRITE(int num) {
  if (written) return;
  written = true;
  g->g[y][x].marks[player_id-1] = num;
}

void Unit::GRAB() {
  if (grabbed) return;
  grabbed = true;
  if (g->g[y][x].zucker > 0) {
    g->g[y][x].zucker-=1;
  }
  carry += 1;
}

void Unit::PUT() {
  if (putted) return;
  putted = true;
  if (g->g[y][x].base == player_id - 1) {
    scores[player_id-1] += carry;
    carry = 0;
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
  int n_steps = 20;
  int n_zucker = 10;
  for (int st = 0; st < n_steps; st++) {
    vector<pair<int, int>> zucker_change;
    // TODO: randomize steps
    for (int z = 0; z < n_zucker; z++) {
      int y = rand()%g.g.size();
      int x = rand()%g.g[0].size();
      if (rand()%100000 < ((int)(100000*g.g[y][x].zucker_prob))) {
        if (g.g[y][x].zucker < 10) {
          g.g[y][x].zucker += 1;
          printf("zucker %d %d %d\n", y, x, g.g[y][x].zucker);
          zucker_change.push_back(make_pair(y, x));
        }
      }
    }
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
        fprintf(flog, "{\"y\": %d, \"x\": %d, \"carry\": %d }%c",
                g.units[i*g.units_per_team+j]->y,
                g.units[i*g.units_per_team+j]->x, 
                g.units[i*g.units_per_team+j]->carry,
                j + 1 == g.units_per_team ? ']' : ',');
      }
      fprintf(flog, "%c", i + 1 == n_players ? ']' : ',');
    }
    fprintf(flog, ", \"zucker\": [");
    for (int i = 0; i < zucker_change.size(); i++) {
      fprintf(flog, "{\"y\": %d, \"x\": %d, \"new_ammount\": %d}",
              zucker_change[i].first, zucker_change[i].second,
              g.g[zucker_change[i].first][zucker_change[i].second].zucker);
      if (i + 1 < zucker_change.size()) fprintf(flog, ",");
    }
    fprintf(flog, "]");
    fprintf(flog, ", \"scores\": [");
    for (int i = 0; i < scores.size(); i++) {
      fprintf(flog, "%d%c", scores[i], i + 1 == scores.size() ? ']' : ',');
    }
    fprintf(flog, ", \"msgs\": [");
    for (int i = 0; i < g.cur_msgs.size(); i++) {
      fprintf(flog, "{\"player_id\": %d, \"from\": %d, \"to\": %d}",
              g.cur_msgs[i].first, g.cur_msgs[i].second.first,
              g.cur_msgs[i].second.second);
      if (i + 1 < g.cur_msgs.size()) {
        fprintf(flog, ",");
      }
    }
    fprintf(flog, "]");
    g.cur_msgs.clear();
    fprintf(flog, "}%c", st + 1 == n_steps ? ']' : ','); 
  }
  fprintf(flog, "}");

  fclose(flog);
}
