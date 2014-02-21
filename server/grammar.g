from compiler_objs import *
%%
parser Proboj:
    ignore:      '\\s+'
    token NUM:   '-?[0-9]+'
    token CALL:  "(PUT|MSG|MOVE)"
    token MSG:   "INBOX"
    token AREA:  "(AREA_PL|AREA_BASE|AREA_WALL|AREA_ZUCK)"
    token RAND:  "RAND"
    token ID:    '[a-zA-Z][a-zA-Z0-9_]*' 
    token END:   "$"
 
    rule goal:  {{ g = [] }}
                (statement {{ g.append(statement) }})*
                END {{ return g }}



    rule statement: assignment";" {{ return assignment }}
                    | call";" {{ return call }}
    rule assignment: ID "=" expr0 {{ return Assignment(Id(ID), expr0) }}
    rule call: CALL"[(]"  {{ e = Call(CALL) }}
                   (expr0 {{ e.add_arg(expr0) }}
                   (","expr0  {{ e.add_arg(expr0) }}
                   )*)?
                   "[)]"   {{ return e }}

    rule expr0: expr1          {{ e = Expr(expr1) }}
                ( "[+]" expr1  {{ e.add_op("+", expr1) }}
                | "-" expr1  {{ e.add_op("-", expr1) }}
                )*  {{ return e }}

    rule expr1: expr2         {{ e = Expr(expr2) }}
                ( "[*]" expr2  {{ e.add_op("*", expr2) }}
                | "/" expr2  {{ e.add_op("/", expr2) }}
                | "%" expr2  {{ e.add_op("%", expr2) }}
                )*  {{ return e }}
                
  
    rule expr2: NUM {{ return Num(int(NUM)) }} |
                "[(]"expr0"[)]" {{ return expr0 }} |
                ID {{ return Id(ID) }} |
                MSG"\\["NUM"\\]" {{ return Msg(int(NUM)) }} | 
                AREA"\\["NUM {{ num1 = int(NUM) }} ","NUM"\\]" {{ return Area(AREA, num1, int(NUM)) }} | 
                RAND {{ return Rand() }}
                
