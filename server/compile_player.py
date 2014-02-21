import grammar
import sys

fp = open(sys.argv[1])

data = fp.read()

x = grammar.parse('goal', data)

for st in x:
  print st.output(2)
