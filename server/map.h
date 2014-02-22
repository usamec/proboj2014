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
  vector<int> marks;
  Point() : wall(false), zucker(0), zucker_prob(0.0), base(-1) {}
};

struct Game;

class Unit {
 public:
  int x, y, id, player_id, carry;
  Game *g;
  bool moved, putted, grabbed, written;

  void Step();
  virtual void RealStep()=0;
  void MOVE(int yy, int xx);
  void WRITE(int num);
  void GRAB();
  void PUT();
  unordered_map<string, int> data;
  unordered_map<int, int> inbox;
  unordered_map<int, unordered_map<int, int>> AREA_PL, AREA_BASE, AREA_WALL, AREA_ZUCK, AREA_MARKS;
};

typedef vector<vector<Point>> Grid;

struct Game {
  Grid g;
  int units_per_team;
  
  vector<Unit*> units;
};



#endif 
