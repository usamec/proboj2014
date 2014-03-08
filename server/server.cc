#include "map.h"
#include "game_config.h"
#include <cstdio>
#include <algorithm>
#include <unordered_map>
#include <cassert>
#include <ctime>

vector<int> scores;
int tick = 0;
int max_tick = 5000;

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
  assert(false);
}

Game LoadGame(char* fn) {
  FILE *f = fopen(fn, "r");
  Game g;
  int r, c;
  scores.resize(n_players);
  vector<int> base_perm(n_players);
  for (int i = 0; i < base_perm.size(); i++) {
    base_perm[i] = i;
  }
  random_shuffle(base_perm.begin(), base_perm.end());
  fscanf(f, "%d %d %d", &r, &c, &g.units_per_team);
  g.g.resize(r, vector<Point>(c));
  for (int i = 0; i < r; i++) {
    for (int j = 0; j < c; j++) {
      double x; fscanf(f, "%lf", &x);
      if (x < 0) {
        g.g[i][j].wall = true;
      } else if (x >= 1) {
        g.g[i][j].base = base_perm[(int)(x)-1]+1;
      }
      else g.g[i][j].zucker_prob = x;
      g.g[i][j].marks.resize(n_players);
    }
  }
  for (int i = 0; i < n_players; i++) {
    for (int j = 0; j < g.units_per_team; j++) {
      int x, y;
      GetEmptyPos(g, i+1, y, x);
      Unit* u = CreatePlayerUnit(i+1);
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
  data["R"] = g->g.size();
  data["C"] = g->g[0].size();
  data["PL_ID"] = player_id;
  data["ID"] = id;
  data["MAX_ID"] = g->units_per_team;
  data["MAX_PLAYER"] = n_players;
  data["CARRY"] = carry;
  data["TICK"] = tick;
  data["MAX_TICK"] = max_tick;
  act = false;
  AREA_PL.clear();
  AREA_BASE.clear();
  AREA_WALL.clear();
  AREA_ZUCK.clear();
  AREA_MARKS.clear();
  int sur = 2;
  for (int i = -sur; i <= sur; i++) {
    for (int j = -sur; j <= sur; j++) {
      if (abs(i) + abs(j) > sur) continue;
      int ry = y + i;
      int rx = x + j;
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

      AREA_BASE[i][j] = g->g[ry][rx].base;
      AREA_WALL[i][j] = g->g[ry][rx].wall;
      AREA_ZUCK[i][j] = g->g[ry][rx].zucker;
      AREA_MARKS[i][j] = g->g[ry][rx].marks[player_id-1];
    }
  }
  RealStep();
  inbox.clear();
}

void Unit::ATTACK(int yy, int xx) {
  if (act) return;
  act = true;
  yy = max(-1, min(1, yy));
  xx = max(-1, min(1, xx));
  int px = x+xx;
  int py = y+yy;
  printf("attack %d %d %d %d\n", xx, yy, px, py);
  for (int i = 0; i < g->units.size(); i++) {
    if (g->units[i]->x == px && g->units[i]->y == py) {
      printf("attack from %d %d to %d %d ff %d %d tt %d %d\n", x, y, px, py, player_id, id,
             g->units[i]->player_id, g->units[i]->id);
      if (rand() % 3 == 0) {
        printf("kill\n");
        g->units[i]->data.clear();
        g->units[i]->inbox.clear();
        g->units[i]->carry = 0;
        int nx, ny;
        g->units[i]->x = -1;
        g->units[i]->y = -1;
        GetEmptyPos(*g, g->units[i]->player_id, ny, nx);
        g->units[i]->y = ny;
        g->units[i]->x = nx;
        g->cur_attacks.push_back(Attack(make_pair(player_id, id),
                                        make_pair(g->units[i]->player_id,
                                                  g->units[i]->id),
                                        true));
      } else {
        g->cur_attacks.push_back(Attack(make_pair(player_id, id),
                                        make_pair(g->units[i]->player_id,
                                                  g->units[i]->id),
                                        false));
      }
    }
  }
}

void Unit::MOVE(int yy, int xx) {
  if (act) return;
  act = true;
  yy = max(-1, min(1, yy));
  xx = max(-1, min(1, xx));
  int px = x;
  int py = y;
  x += xx;
  y += yy;
  printf("move %d %d %d %d %d %d\n", player_id, id, xx, yy, x, y);
  x = max(0, min((int)g->g[0].size()-1, x));
  y = max(0, min((int)g->g.size()-1, y));
  // TODO: check other units
  bool other_unit = false;
  for (int i = 0; i < g->units.size(); i++) {
    if (g->units[i] == this) continue;
    if (g->units[i]->x == x && g->units[i]->y == y) {
      other_unit = true;
    }
  }
  if (g->g[y][x].wall == true || other_unit == true) {
    x = px;
    y = py;
  }
}

void Unit::WRITE(int num) {
  if (act) return;
  act = true;
  g->g[y][x].marks[player_id-1] = num;
}

void Unit::GRAB() {
  if (act) return;
  printf("GRAB ");
  act = true;
  if (g->g[y][x].zucker > 0 && carry < 10) {
    printf("OK");
    g->g[y][x].zucker-=1;
    carry += 1;
  }
  printf("\n");
}

void Unit::PUT() {
  if (act) return;
  act = true;
  printf("PUT ");
  if (g->g[y][x].base == player_id) {
    printf("OK %d", carry);
    scores[player_id-1] += carry;
    carry = 0;
  }
  printf("\n");
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
  srand(time(NULL));
  Game g = LoadGame(argv[1]);
  FILE* flog = fopen(argv[2], "w");
  fprintf(flog, "{");
  LogMap(flog, g);
  printf("init done\n");

  vector<pair<int, int>> zucker_opts;
  for (int i = 0; i < g.g.size(); i++) {
    for (int j = 0; j < g.g[i].size(); j++) {
      if (g.g[i][j].zucker_prob > 0) {
        zucker_opts.push_back(make_pair(i, j)); 
      }
    }
  }

  fprintf(flog, ", \"steps\": [");
  int n_steps = max_tick;
  int n_zucker = 10;
  for (int st = 0; st < n_steps; st++) {
    tick = st + 1;
    vector<pair<int, int>> zucker_change;
    // TODO: randomize steps
    for (int z = 0; z < n_zucker; z++) {
      int co = rand()%zucker_opts.size();
      int y = zucker_opts[co].first;
      int x = zucker_opts[co].second;
      if (rand()%100000 < ((int)(100000*g.g[y][x].zucker_prob))) {
        if (g.g[y][x].zucker < 10) {
          g.g[y][x].zucker += 1;
          printf("zucker %d %d %d\n", y, x, g.g[y][x].zucker);
          zucker_change.push_back(make_pair(y, x));
        }
      }
    }
    g.units[st%g.units.size()]->Step();

    for (int i = 0; i < g.units.size(); i++) {
      printf("(%d, %d) ", g.units[i]->x, g.units[i]->y);
    }
    printf("\n");

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
    fprintf(flog, ", \"attacks\": [");
    for (int i = 0; i < g.cur_attacks.size(); i++) {
      fprintf(flog, "{\"from_player\": %d, \"from_id\": %d, "
                    "\"to_player\": %d, \"to_id\": %d, \"success\": %d}",
                    g.cur_attacks[i].from.first, g.cur_attacks[i].from.second,
                    g.cur_attacks[i].to.first, g.cur_attacks[i].to.second,
                    (int)g.cur_attacks[i].success);
      if (i + 1 < g.cur_msgs.size()) {
        fprintf(flog, ",");
      }
    }
    fprintf(flog, "]");
    g.cur_attacks.clear();
    fprintf(flog, "}%c", st + 1 == n_steps ? ']' : ','); 
  }
  fprintf(flog, "}");

  fclose(flog);

  string sc(argv[2]);
  sc += ".scr";
  FILE *fscr = fopen(sc.c_str(), "w");
  for (int i = 0; i < scores.size(); i++) {
    fprintf(fscr, "%d\n", scores[i]);
  }
  fclose(fscr);
}
