
#include "map.h"
#include <cstdlib>

class Player1 : public Unit {
 public:
  virtual void RealStep() {
    MOVE(((rand()%3)-1),((rand()%3)-1));

  }
};

