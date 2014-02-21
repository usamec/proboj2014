from compiler_objs import *

# Begin -- grammar generated by Yapps
import sys, re
from yapps import runtime

class ProbojScanner(runtime.Scanner):
    patterns = [
        ('"\\\\]"', re.compile('\\]')),
        ('"\\\\["', re.compile('\\[')),
        ('"%"', re.compile('%')),
        ('"/"', re.compile('/')),
        ('"[*]"', re.compile('[*]')),
        ('"-"', re.compile('-')),
        ('"[+]"', re.compile('[+]')),
        ('"[)]"', re.compile('[)]')),
        ('","', re.compile(',')),
        ('"[(]"', re.compile('[(]')),
        ('"="', re.compile('=')),
        ('";"', re.compile(';')),
        ('\\s+', re.compile('\\s+')),
        ('NUM', re.compile('[0-9]+')),
        ('CALL', re.compile('(RAND|PUT|MSG)')),
        ('MSG', re.compile('INBOX')),
        ('AREA', re.compile('AREA')),
        ('ID', re.compile('[a-zA-Z][a-zA-Z0-9_]*')),
        ('END', re.compile('$')),
    ]
    def __init__(self, str,*args,**kw):
        runtime.Scanner.__init__(self,None,{'\\s+':None,},str,*args,**kw)

class Proboj(runtime.Parser):
    Context = runtime.Context
    def goal(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'goal', [])
        g = []
        while self._peek('END', 'ID', 'CALL', context=_context) != 'END':
            statement = self.statement(_context)
            g.append(statement)
        END = self._scan('END', context=_context)
        return g

    def statement(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'statement', [])
        _token = self._peek('ID', 'CALL', context=_context)
        if _token == 'ID':
            assignment = self.assignment(_context)
            self._scan('";"', context=_context)
            return assignment
        else: # == 'CALL'
            call = self.call(_context)
            self._scan('";"', context=_context)
            return call

    def assignment(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'assignment', [])
        ID = self._scan('ID', context=_context)
        self._scan('"="', context=_context)
        expr0 = self.expr0(_context)
        return Assignment(Id(ID), expr0)

    def call(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'call', [])
        CALL = self._scan('CALL', context=_context)
        self._scan('"[(]"', context=_context)
        e = Call(CALL)
        if self._peek('"[)]"', '","', 'NUM', '"[(]"', 'ID', 'MSG', 'AREA', context=_context) not in ['"[)]"', '","']:
            expr0 = self.expr0(_context)
            e.add_arg(expr0)
            while self._peek('","', '"[)]"', context=_context) == '","':
                self._scan('","', context=_context)
                expr0 = self.expr0(_context)
                e.add_arg(expr0)
        self._scan('"[)]"', context=_context)
        return e

    def expr0(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'expr0', [])
        expr1 = self.expr1(_context)
        e = Expr(expr1)
        while self._peek('"[+]"', '"-"', '"[)]"', '","', '";"', context=_context) in ['"[+]"', '"-"']:
            _token = self._peek('"[+]"', '"-"', context=_context)
            if _token == '"[+]"':
                self._scan('"[+]"', context=_context)
                expr1 = self.expr1(_context)
                e.add_op("+", expr1)
            else: # == '"-"'
                self._scan('"-"', context=_context)
                expr1 = self.expr1(_context)
                e.add_op("-", expr1)
        return e

    def expr1(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'expr1', [])
        expr2 = self.expr2(_context)
        e = Expr(expr2)
        while self._peek('"[*]"', '"/"', '"%"', '"[+]"', '"-"', '"[)]"', '","', '";"', context=_context) in ['"[*]"', '"/"', '"%"']:
            _token = self._peek('"[*]"', '"/"', '"%"', context=_context)
            if _token == '"[*]"':
                self._scan('"[*]"', context=_context)
                expr2 = self.expr2(_context)
                e.add_op("*", expr2)
            elif _token == '"/"':
                self._scan('"/"', context=_context)
                expr2 = self.expr2(_context)
                e.add_op("/", expr2)
            else: # == '"%"'
                self._scan('"%"', context=_context)
                expr2 = self.expr2(_context)
                e.add_op("%", expr2)
        return e

    def expr2(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'expr2', [])
        _token = self._peek('NUM', '"[(]"', 'ID', 'MSG', 'AREA', context=_context)
        if _token == 'NUM':
            NUM = self._scan('NUM', context=_context)
            return Num(int(NUM))
        elif _token == '"[(]"':
            self._scan('"[(]"', context=_context)
            expr0 = self.expr0(_context)
            self._scan('"[)]"', context=_context)
            return expr0
        elif _token == 'ID':
            ID = self._scan('ID', context=_context)
            return Id(ID)
        elif _token == 'MSG':
            MSG = self._scan('MSG', context=_context)
            self._scan('"\\\\["', context=_context)
            NUM = self._scan('NUM', context=_context)
            self._scan('"\\\\]"', context=_context)
            return Msg(int(NUM))
        else: # == 'AREA'
            AREA = self._scan('AREA', context=_context)
            self._scan('"\\\\["', context=_context)
            NUM = self._scan('NUM', context=_context)
            num1 = int(NUM)
            self._scan('","', context=_context)
            NUM = self._scan('NUM', context=_context)
            self._scan('"\\\\]"', context=_context)
            return Area(num1, int(NUM))


def parse(rule, text):
    P = Proboj(ProbojScanner(text))
    return runtime.wrap_error_reporter(P, rule)

if __name__ == '__main__':
    from sys import argv, stdin
    if len(argv) >= 2:
        if len(argv) >= 3:
            f = open(argv[2],'r')
        else:
            f = stdin
        print parse(argv[1], f.read())
    else: print >>sys.stderr, 'Args:  <rule> [<filename>]'
# End -- grammar generated by Yapps
