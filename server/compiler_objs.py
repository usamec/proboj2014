keywords = ["RAND", "PUT", "MSG", "AREA"]

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
    return 'inbox[%d]' % self.index

class Area:
  def __init__(self, type, r, c):
    self.type = type
    self.r = r
    self.c = c

  def output(self):
    return '%s[%d][%d]' % (self.type, self.r, self.c)
