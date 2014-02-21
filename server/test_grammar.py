import grammar
import pprint

pp = pprint.PrettyPrinter()

pp.pprint(grammar.parse('goal', 'wtf = 7 + 5 + 4 / (7+2) * 3; RAND(4, 7);'))
pp.pprint(grammar.parse('goal', 'Q = INBOX[47];'))
pp.pprint(grammar.parse('goal', 'Q = AREA[47,42];'))

x = grammar.parse('goal', 'x = 4 * (7/4) + y * 8;')

print x[0].output(2)
