
#include "map.h"
#include <cstdlib>

class Player1 : public Unit {
 public:
  virtual void RealStep() {
    if ((AREA_PL[1][0]>0)) {
      ATTACK(1,0);
    } else if (((AREA_ZUCK[0][0]>0)&&(data["CARRY"]<10))) {
      GRAB();
    } else if (((AREA_BASE[0][0]==data["PL_ID"])&&(data["CARRY"]>0))) {
      PUT();
    } else {
      MOVE(((rand()%3)-1),((rand()%3)-1));
    }

  }
};

