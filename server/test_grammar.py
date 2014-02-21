import grammar
import pprint

pp = pprint.PrettyPrinter()

#pp.pprint(grammar.parse('goal', 'wtf = 7 + 5 + 4 / (7+2) * 3; RAND(4, 7);'))
#pp.pprint(grammar.parse('goal', 'Q = INBOX[47];'))
#pp.pprint(grammar.parse('goal', 'Q = AREA[47,42];'))

x = grammar.parse('goal', 'x = AREA[-2,-3] * (7/4) + y * 8 + INBOX[5] + RAND % 47; MOVE(-1,0);')

for st in x:
  print st.output(2)
