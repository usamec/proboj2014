from compiler_objs import *
%%
parser Proboj:
    ignore:      '\\s+'
    token NUM:   '-?[0-9]+'
    token ELIF:  "elif"
    token IF:    "if"
    token ELSE:  "else"
    token CALL:  "(PUT|MOVE|GRAB|WRITE|ATTACK)"
    token MSGCALL: "MSG"
    token MSG:   "INBOX"
    token AREA:  "(AREA_PL|AREA_BASE|AREA_WALL|AREA_ZUCK|AREA_MARKS)"
    token RAND:  "RAND"
    token RET: "return"
    token DEF:   "def"
    token ID:    '[a-zA-Z][a-zA-Z0-9_]*' 
    token END:   "$"
 
    rule goal:  {{ g = [] }}
                (statement {{ g.append(statement) }})*
                END {{ return g }}



    rule statement: assignment";" {{ return assignment }}
                    | call";" {{ return call }}
                    | msgcall";" {{ return msgcall }}
                    | conditional {{ return conditional }}
                    | fdef {{ return fdef }}
                    | ret {{ return ret }}

    rule ret: RET exprcomp";" {{ return Ret(exprcomp); }}

    rule msgcall: MSGCALL"[(]"exprcomp  {{ e = MsgCall(exprcomp) }}
                         (","exprcomp  {{ e.add_arg(exprcomp) }}
                         )*
                        "[)]"   {{ return e }}

    rule fdef: DEF ID"[(]" {{ e = Fdef(ID) }}
               (ID {{ e.add_arg(ID) }}
               (","ID  {{ e.add_arg(ID) }}
               )*)?
               "[)]" block {{ e.add_block(block) }}
               {{ return e }}
                

    rule conditional: IF"[(]" exprcomp "[)]" block {{ i = Cond(exprcomp, block) }}
                      (ELIF"[(]" exprcomp "[)]" block {{ i.add_elif(exprcomp, block) }})*
                      (ELSE block {{i.add_else(block) }} )?
                      {{ return i }}

    rule block: "{" {{ g = [] }} (statement {{ g.append(statement) }})*
                "}" {{ return g }}

    rule assignment: ID "=" exprcomp {{ return Assignment(Id(ID), exprcomp) }}
    rule call: CALL"[(]"  {{ e = Call(CALL) }}
                   (exprcomp {{ e.add_arg(exprcomp) }}
                   (","exprcomp  {{ e.add_arg(exprcomp) }}
                   )*)?
                   "[)]"   {{ return e }}

    rule exprcomp: expr00          {{ e = Expr(expr00) }}
                ( "&&" expr00  {{ e.add_op("&&", expr00) }}
                | "\|\|" expr00  {{ e.add_op("||", expr00) }}
                )*  {{ return e }}
   
    rule expr00:   expr0 {{ e = Expr(expr0) }}
                   ( "==" expr0  {{ e.add_op("==", expr0) }}
                   | "<=" expr0  {{ e.add_op("<=", expr0) }}
                   | "<" expr0  {{ e.add_op("<", expr0) }}
                   | ">" expr0  {{ e.add_op(">", expr0) }}
                   | ">=" expr0  {{ e.add_op(">=", expr0) }}
                   | "!=" expr0  {{ e.add_op("!=", expr0) }})* 
		    {{ return e }}


    rule expr0: expr1          {{ e = Expr(expr1) }}
                ( "[+]" expr1  {{ e.add_op("+", expr1) }}
                | "-" expr1  {{ e.add_op("-", expr1) }}
                )*  {{ return e }}

    rule expr1: expr2         {{ e = Expr(expr2) }}
                ( "[*]" expr2  {{ e.add_op("*", expr2) }}
                | "/" expr2  {{ e.add_op("/", expr2) }}
                | "%" expr2  {{ e.add_op("%", expr2) }}
                )*  {{ return e }}
                
    rule expr2: exprf {{ return exprf  }}
                | "!"exprf {{ return Neg(exprf) }}

    rule exprf: exprel {{ e = exprel }}
                ("[(]"  {{ e = Exprf(exprel) }}
                (exprcomp {{ e.add_arg(exprcomp) }}
                (","exprcomp  {{ e.add_arg(exprcomp) }}
                )*)?
                "[)]")?   {{ return e }}


    rule exprel: NUM {{ return Num(int(NUM)) }} |
                "[(]"exprcomp"[)]" {{ return exprcomp }} |
                ID {{ return Id(ID) }} |
                MSG"\\["exprcomp"\\]" {{ return Msg(exprcomp) }} | 
                AREA"\\["exprcomp {{ num1 = exprcomp }} ","exprcomp"\\]" {{ return Area(AREA, num1, exprcomp) }} | 
                RAND {{ return Rand() }}
                
