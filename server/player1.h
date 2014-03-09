
#include "map.h"
#include <cstdlib>

class Player1 : public Unit {
 public:
  virtual void RealStep() {
    class min { unordered_map<string, int> data; public: int operator()(int a,int b) {
      data["a"] = a;
      data["b"] = b;
      data["d"]=(data["a"]+data["b"]);
      if ((data["a"]<data["b"])) {
        return data["a"];
      }
      return data["b"];
    }};
    min omin;
    data["c"]=omin(4,7);
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

