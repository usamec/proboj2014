import sys

keywords = ["RAND", "PUT", "MSG", "AREA"]

functions = set()

class Cond:
  def __init__(self, if_expr, if_block):
    self.if_expr = if_expr
    self.if_block = if_block
    self.elifs = []
    self.else_block = None

  def add_elif(self, expr, block):
    self.elifs.append((expr, block))

  def add_else(self, block):
    self.else_block = block

  def output(self, indent):
    ret_parts = []
    ret_parts.append(" "*indent)
    ret_parts.append("if (")
    ret_parts.append(self.if_expr.output())
    ret_parts.append(") {\n")
    for x in self.if_block:
      ret_parts.append(x.output(indent+2))
      ret_parts.append("\n");
    ret_parts.append(" "*indent)
    ret_parts.append("}")
    for el in self.elifs:
      ret_parts.append(" else if (")
      ret_parts.append(el[0].output())
      ret_parts.append(") {\n")
      for x in el[1]:
        ret_parts.append(x.output(indent+2))
        ret_parts.append("\n");
      ret_parts.append(" "*indent)
      ret_parts.append("}")
    
    if self.else_block:
      ret_parts.append(" else {\n")
      for x in self.else_block:
        ret_parts.append(x.output(indent+2))
        ret_parts.append("\n");
      ret_parts.append(" "*indent)
      ret_parts.append("}")
      

    return ''.join(ret_parts)

class Expr:
  def __init__(self, left):
    self.left = left
    self.ops = []

  def add_op(self, op, right):
    self.ops.append((op, right))

  def output(self):
    ret_parts = []
    if len(self.ops) > 0:
      ret_parts.append("(")
    ret_parts += self.left.output()
    for x in self.ops:
      ret_parts.append(x[0])
      ret_parts += x[1].output()
    if len(self.ops) > 0:
      ret_parts.append(")")
    return ''.join(ret_parts)

class Assignment:
  def __init__(self, left, right):
    self.left = left
    self.right = right

  def output(self, indent):
    ret_parts = []
    ret_parts.append(" "*indent)
    ret_parts += self.left.output()
    ret_parts += ["="]
    ret_parts += self.right.output()
    ret_parts.append(";")
    return ''.join(ret_parts)


class MsgCall:
  def __init__(self, who):
    self.who = who
    self.args = []

  def add_arg(self, arg):
    self.args.append(arg)

  def output(self, indent):
    ret_parts = []
    ret_parts.append(" "*indent)
    ret_parts.append("MSG(")
    ret_parts.append(self.who.output())
    ret_parts.append(", vector<int>({");
    args_str = [x.output() for x in self.args]
    ret_parts.append(",".join(args_str))
    ret_parts.append("}));")
    return ''.join(ret_parts)

class Call:
  def __init__(self, what):
    self.what = what
    self.args = []

  def add_arg(self, arg):
    self.args.append(arg)

  def output(self, indent):
    ret_parts = []
    ret_parts.append(" "*indent)
    ret_parts.append(self.what)
    ret_parts.append("(")
    args_str = [x.output() for x in self.args]
    ret_parts.append(",".join(args_str))
    ret_parts.append(");")
    return ''.join(ret_parts)

class Num:
  def __init__(self, what):
    self.what = what

  def output(self):
    return str(self.what)

class Rand:
  def output(self):
    return "rand()"

class Neg:
  def __init__(self, expr):
    self.expr = expr

  def output(self):
    return "!" + self.expr.output()

class Id:
  def __init__(self, what):
    self.what = what

  def output(self):
    if self.what in keywords:
      raise Exception("Pouzil is keyword ako premennu")
    return 'data["%s"]' % self.what

class Msg:
  def __init__(self, index):
    self.index = index

  def output(self):
    return 'inbox[%s]' % self.index.output()

class Area:
  def __init__(self, type, r, c):
    self.type = type
    self.r = r
    self.c = c

  def output(self):
    return '%s[%s][%s]' % (self.type, self.r.output(), self.c.output())

class Exprf:
  def __init__(self, expr):
    self.expr = expr
    self.args = []

  def add_arg(self, expr):
    self.args.append(expr)

  def output(self):
    global functions
    if not isinstance(self.expr, Id):
      print >>sys.stderr, "zle volanie funkcie, volas funkciu na nieco divne"
      sys.exit(1)
    name = self.expr.what
    if name not in functions:
      print >>sys.stderr, "zle volanie funkcie, neznama func", name
      sys.exit(1)

    ret_parts = []
    ret_parts.append("o%s(" % name)
    ret_parts.append(",".join([x.output() for x in self.args]))
    ret_parts.append(")")
    return "".join(ret_parts)

class Fdef:
  def __init__(self, id):
    self.name = id
    self.args = []
    self.block = None

  def add_arg(self, id):
    self.args.append(id)

  def add_block(self, block):
    self.block = block

  def output(self, indent):
    global functions
    ret_parts = []
    ret_parts.append(" "*indent)
    ret_parts.append("class %s { unordered_map<string, int> data; public: int operator()(" % (self.name))
    ret_parts.append(",".join(["int "+x for x in self.args]))
    ret_parts.append(") {\n")
    for x in self.args:
      ret_parts.append(" "*(indent+2))    
      ret_parts.append('data["%s"] = %s;\n' % (x, x))

    for x in functions:
      ret_parts.append(" "*(indent+2))
      ret_parts.append('%s o%s;\n' % (x, x))
    for x in self.block:
      ret_parts.append(x.output(indent+2))
      ret_parts.append("\n");
    ret_parts.append(" "*indent)
    ret_parts.append("}};\n")
    ret_parts.append(" "*indent)
    ret_parts.append("%s o%s;" % (self.name, self.name))

    functions.add(self.name)
    return "".join(ret_parts)

class Ret:
  def __init__(self, expr):
    self.expr = expr

  def output(self, indent):
    ret_parts = []
    ret_parts.append(" "*indent)
    ret_parts.append("return ")
    ret_parts.append(self.expr.output())
    ret_parts.append(";");
    return ''.join(ret_parts)

