
#include "map.h"
#include <cstdlib>

class Player1 : public Unit {
 public:
  virtual void RealStep() {
    if ((data["ID"]==1)) {
      data["a"]=AREA_PL[-1][-1];
      data["b"]=inbox[3];
      MOVE(((rand()%3)-1),((rand()%3)-1));
      ATTACK(1,0);
      MSG(2, vector<int>({47,42}));
    } else if ((data["ID"]==2)) {
      data["c"]=data["b"];
    } else {
      data["d"]=(data["c"]+4);
    }

  }
};

