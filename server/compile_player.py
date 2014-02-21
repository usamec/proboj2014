import grammar
import sys

prefix = """
#include "map.h"
#include <cstdlib>

class Player%s : public Unit {
 public:
  virtual void RealStep() {"""

suffix = """
  }
};
"""

fp = open(sys.argv[1])

data = fp.read()

x = grammar.parse('goal', data)

print prefix % sys.argv[2]

for st in x:
  print st.output(4)

print suffix
