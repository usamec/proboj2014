
#include "map.h"
#include <cstdlib>

class Player1 : public Unit {
 public:
  virtual void RealStep() {
    class max { unordered_map<string, int> data; public: int operator()(int a,int b,int c,int d,int e,int f,int g,int h) {
      data["a"] = a;
      data["b"] = b;
      data["c"] = c;
      data["d"] = d;
      data["e"] = e;
      data["f"] = f;
      data["g"] = g;
      data["h"] = h;
      if ((data["a"]>=data["u"])) {
        data["u"]=data["a"];
        data["y"]=1;
      }
      if ((data["b"]>=data["u"])) {
        data["u"]=data["b"];
        data["y"]=2;
      }
      if ((data["c"]>=data["u"])) {
        data["u"]=data["c"];
        data["y"]=3;
      }
      if ((data["d"]>=data["u"])) {
        data["u"]=data["d"];
        data["y"]=4;
      }
      if ((data["e"]>=data["u"])) {
        data["u"]=data["e"];
        data["y"]=5;
      }
      if ((data["f"]>=data["u"])) {
        data["u"]=data["f"];
        data["y"]=6;
      }
      if ((data["g"]>=data["u"])) {
        data["u"]=data["g"];
        data["y"]=7;
      }
      if ((data["h"]>=data["u"])) {
        data["u"]=data["h"];
        data["y"]=8;
      }
      return data["y"];
    }};
    max omax;
    class min { unordered_map<string, int> data; public: int operator()(int a,int b,int c,int d,int e,int f,int g,int h) {
      data["a"] = a;
      data["b"] = b;
      data["c"] = c;
      data["d"] = d;
      data["e"] = e;
      data["f"] = f;
      data["g"] = g;
      data["h"] = h;
      max omax;
      data["u"]=12345;
      if ((data["a"]==0)) {
        data["a"]=12345;
      }
      if ((data["b"]==0)) {
        data["b"]=12345;
      }
      if ((data["c"]==0)) {
        data["c"]=12345;
      }
      if ((data["d"]==0)) {
        data["d"]=12345;
      }
      if ((data["e"]==0)) {
        data["e"]=12345;
      }
      if ((data["f"]==0)) {
        data["f"]=12345;
      }
      if ((data["g"]==0)) {
        data["g"]=12345;
      }
      if ((data["h"]==0)) {
        data["h"]=12345;
      }
      if ((data["a"]<=data["u"])) {
        data["u"]=data["a"];
        data["y"]=1;
      }
      if ((data["b"]<=data["u"])) {
        data["u"]=data["b"];
        data["y"]=2;
      }
      if ((data["c"]<=data["u"])) {
        data["u"]=data["c"];
        data["y"]=3;
      }
      if ((data["d"]<=data["u"])) {
        data["u"]=data["d"];
        data["y"]=4;
      }
      if ((data["e"]<=data["u"])) {
        data["u"]=data["e"];
        data["y"]=5;
      }
      if ((data["f"]<=data["u"])) {
        data["u"]=data["f"];
        data["y"]=6;
      }
      if ((data["g"]<=data["u"])) {
        data["u"]=data["g"];
        data["y"]=7;
      }
      if ((data["h"]<=data["u"])) {
        data["u"]=data["h"];
        data["y"]=8;
      }
      return data["y"];
    }};
    min omin;
    class min2 { unordered_map<string, int> data; public: int operator()(int a,int b,int c,int d,int e,int f,int g,int h) {
      data["a"] = a;
      data["b"] = b;
      data["c"] = c;
      data["d"] = d;
      data["e"] = e;
      data["f"] = f;
      data["g"] = g;
      data["h"] = h;
      max omax;
      min omin;
      data["u"]=12345;
      if ((data["a"]==0)) {
        data["a"]=12345;
      }
      if ((data["b"]==0)) {
        data["b"]=12345;
      }
      if ((data["c"]==0)) {
        data["c"]=12345;
      }
      if ((data["d"]==0)) {
        data["d"]=12345;
      }
      if ((data["e"]==0)) {
        data["e"]=12345;
      }
      if ((data["f"]==0)) {
        data["f"]=12345;
      }
      if ((data["g"]==0)) {
        data["g"]=12345;
      }
      if ((data["h"]==0)) {
        data["h"]=12345;
      }
      if ((data["a"]<=data["u"])) {
        data["u"]=data["a"];
        data["y"]=1;
      }
      if ((data["b"]<=data["u"])) {
        data["u"]=data["b"];
        data["y"]=2;
      }
      if ((data["c"]<=data["u"])) {
        data["u"]=data["c"];
        data["y"]=3;
      }
      if ((data["d"]<=data["u"])) {
        data["u"]=data["d"];
        data["y"]=4;
      }
      if ((data["e"]<=data["u"])) {
        data["u"]=data["e"];
        data["y"]=5;
      }
      if ((data["f"]<=data["u"])) {
        data["u"]=data["f"];
        data["y"]=6;
      }
      if ((data["g"]<=data["u"])) {
        data["u"]=data["g"];
        data["y"]=7;
      }
      if ((data["h"]<=data["u"])) {
        data["u"]=data["h"];
        data["y"]=8;
      }
      return data["u"];
    }};
    min2 omin2;
    if ((AREA_PL[0][1]>0)) {
      ATTACK(0,1);
    } else if ((AREA_PL[0][-1]>0)) {
      ATTACK(0,-1);
    } else if ((AREA_PL[1][0]>0)) {
      ATTACK(1,0);
    } else if ((AREA_PL[1][1]>0)) {
      ATTACK(1,1);
    } else if ((AREA_PL[1][-1]>0)) {
      ATTACK(1,-1);
    } else if ((AREA_PL[-1][0]>0)) {
      ATTACK(-1,0);
    } else if ((AREA_PL[-1][1]>0)) {
      ATTACK(-1,1);
    } else if ((AREA_PL[-1][-1]>0)) {
      ATTACK(-1,-1);
    }
    if (((AREA_BASE[0][0]==data["PL_ID"])&&(AREA_MARKS[0][0]==0))) {
      WRITE(1);
    }
    if ((((AREA_MARKS[0][0]>(omin2(AREA_MARKS[0][1],AREA_MARKS[1][1],AREA_MARKS[-1][1],AREA_MARKS[-1][0],AREA_MARKS[1][0],AREA_MARKS[-1][-1],AREA_MARKS[0][-1],AREA_MARKS[1][-1])+1))&&(AREA_BASE[0][0]!=data["PL_ID"]))||((AREA_MARKS[0][0]==0)&&(AREA_BASE[0][0]!=data["PL_ID"])))) {
      WRITE((omin2(AREA_MARKS[0][1],AREA_MARKS[1][1],AREA_MARKS[-1][1],AREA_MARKS[-1][0],AREA_MARKS[1][0],AREA_MARKS[-1][-1],AREA_MARKS[0][-1],AREA_MARKS[1][-1])+1));
    }
    if (((AREA_BASE[0][0]==data["PL_ID"])&&(data["CARRY"]>0))) {
      PUT();
    }
    if ((data["CARRY"]==10)) {
      data["minimum"]=omin(AREA_MARKS[0][1],AREA_MARKS[1][1],AREA_MARKS[-1][1],AREA_MARKS[-1][0],AREA_MARKS[1][0],AREA_MARKS[-1][-1],AREA_MARKS[0][-1],AREA_MARKS[1][-1]);
      if (((data["minimum"]==1)&&(AREA_PL[0][1]==0))) {
        MOVE(0,1);
      } else if (((data["minimum"]==2)&&(AREA_PL[1][1]==0))) {
        MOVE(1,1);
      } else if (((data["minimum"]==3)&&(AREA_PL[-1][1]==0))) {
        MOVE(-1,1);
      } else if (((data["minimum"]==4)&&(AREA_PL[-1][0]==0))) {
        MOVE(-1,0);
      } else if (((data["minimum"]==5)&&(AREA_PL[1][0]==0))) {
        MOVE(1,0);
      } else if (((data["minimum"]==6)&&(AREA_PL[-1][-1]==0))) {
        MOVE(-1,-1);
      } else if (((data["minimum"]==7)&&(AREA_PL[0][-1]==0))) {
        MOVE(0,-1);
      } else if (((data["minimum"]==8)&&(AREA_PL[1][-1]==0))) {
        MOVE(1,-1);
      }
    }
    if ((data["CARRY"]<10)) {
      if ((AREA_ZUCK[0][0]>0)) {
        GRAB();
      } else if (((AREA_ZUCK[0][-1]>0)&&(AREA_PL[0][-1]==0))) {
        MOVE(0,-1);
      } else if (((AREA_ZUCK[0][1]>0)&&(AREA_PL[0][1]==0))) {
        MOVE(0,1);
      } else if (((AREA_ZUCK[0][2]>0)&&(AREA_PL[0][1]==0))) {
        MOVE(0,2);
      } else if (((AREA_ZUCK[1][0]>0)&&(AREA_PL[1][0]==0))) {
        MOVE(1,-1);
      } else if (((AREA_ZUCK[1][1]>0)&&(AREA_PL[1][1]==0))) {
        MOVE(1,1);
      } else if (((AREA_ZUCK[2][0]>0)&&(AREA_PL[1][0]==0))) {
        MOVE(1,0);
      } else if (((AREA_ZUCK[-1][0]>0)&&(AREA_PL[-1][0]==0))) {
        MOVE(-1,0);
      } else if (((AREA_ZUCK[-1][1]>0)&&(AREA_PL[-1][1]==0))) {
        MOVE(-1,1);
      } else if (((AREA_ZUCK[-1][-1]>0)&&(AREA_PL[-1][-1]==0))) {
        MOVE(-1,-1);
      } else if (((AREA_ZUCK[-2][0]>0)&&(AREA_PL[-1][0]==0))) {
        MOVE(-1,0);
      } else if (((AREA_ZUCK[0][-2]>0)&&(AREA_PL[0][-1]==0))) {
        MOVE(0,-1);
      }
    }
    if (((AREA_MARKS[0][1]==0)&&(AREA_WALL[0][1]==0)&&(AREA_PL[0][1]==0)&&((data["X"]+1)<data["C"]))) {
      MOVE(0,1);
    }
    if (((AREA_MARKS[1][1]==0)&&(AREA_WALL[1][1]==0)&&(AREA_PL[1][1]==0)&&((data["X"]+1)<data["C"])&&((data["Y"]+1)<data["R"]))) {
      MOVE(1,1);
    }
    if (((AREA_MARKS[1][0]==0)&&(AREA_WALL[1][0]==0)&&(AREA_PL[1][0]==0)&&((data["Y"]+1)<data["R"]))) {
      MOVE(1,0);
    }
    if (((AREA_MARKS[1][-1]==0)&&(AREA_WALL[1][-1]==0)&&(AREA_PL[1][-1]==0)&&((data["Y"]+1)<data["R"])&&(data["X"]>0))) {
      MOVE(1,-1);
    }
    if (((AREA_MARKS[0][-1]==0)&&(AREA_WALL[0][-1]==0)&&(AREA_PL[0][-1]==0)&&(data["X"]>0))) {
      MOVE(0,-1);
    }
    if (((AREA_MARKS[-1][-1]==0)&&(AREA_WALL[-1][-1]==0)&&(AREA_PL[-1][-1]==0)&&(data["X"]>0)&&(data["Y"]>0))) {
      MOVE(-1,-1);
    }
    if (((AREA_MARKS[-1][0]==0)&&(AREA_WALL[-1][0]==0)&&(AREA_PL[-1][0]==0)&&(data["Y"]>0))) {
      MOVE(-1,0);
    }
    if (((AREA_MARKS[-1][1]==0)&&(AREA_WALL[-1][1]==0)&&(AREA_PL[-1][1]==0)&&(data["Y"]>0)&&((data["X"]+1)<data["C"]))) {
      MOVE(-1,1);
    }
    MOVE(((rand()%3)-1),((rand()%3)-1));

  }
};

