
#include "map.h"
#include <cstdlib>

class Player1 : public Unit {
 public:
  virtual void RealStep() {
    if ((AREA_PL[1][0]>0)) {
      ATTACK(1,0);
    } else if ((AREA_PL[1][0]>0)) {
      ATTACK(1,0);
    } else {
      MOVE(((rand()%3)-1),((rand()%3)-1));
    }

  }
};

