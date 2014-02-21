#ifndef MAP_H__
#define MAP_H__

#include <vector>
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
};

typedef vector<vector<Point>> Grid;

struct Game {
  Grid g;
  int units_per_team;
  
  vector<Unit*> units;
};



#endif 
