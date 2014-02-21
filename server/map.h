#ifndef MAP_H__
#define MAP_H__

#include <string>
#include <vector>
#include <unordered_map>
using namespace std;

struct Point {
  bool wall;
  int zucker;
  double zucker_prob;
  int base;
  Point() : wall(false), zucker(0), zucker_prob(0.0), base(-1) {}
};

struct Game;

class Unit {
 public:
  int x, y, id, player_id;
  Game *g;

  void Step();
  virtual void RealStep()=0;
  void MOVE(int yy, int xx);
  unordered_map<string, int> data;
  unordered_map<int, int> inbox;
  unordered_map<int, unordered_map<int, int>> area;
};

typedef vector<vector<Point>> Grid;

struct Game {
  Grid g;
  int units_per_team;
  
  vector<Unit*> units;
};



#endif 
