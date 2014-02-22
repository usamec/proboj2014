
#include "map.h"
#include <cstdlib>

class Player1 : public Unit {
 public:
  virtual void RealStep() {
    data["a"]=AREA_PL[-1][-1];
    MOVE(((rand()%3)-1),((rand()%3)-1));

  }
};

