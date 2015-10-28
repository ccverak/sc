# -----------------------------------------------------------------------------
# sclex.py
# Analizador lexicologico para sc (pseudo - c)
# autor Carlos Castellanos Vera
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

import ply.lex as lex

class Scanner(object):
    __lexer = None
    errorCount = 0
    
    #Tokens
    reserved = {
       'read' : 'READ',
       'write' : 'WRITE',
       'if' : 'IF',
       'else' : 'ELSE',
       'for' : 'FOR',
       'while' : 'WHILE',
       'true' : 'TBOOLEAN',
       'false' : 'FBOOLEAN'
    }
    
    tokens = [
        'PUNTO_Y_COMA', 'SU', 'RE', 'MULT', 'DIV', 'MOD', 'ASIG', 'IDENT', 'REAL', 'ENTERO',
        'COMENT', 'PAR_AB', 'PAR_CERR', 'LLAVE_AB', 'LLAVE_CERR',
        'IGUAL_IGUAL', 'DISTINTO', 'MENOR_QUE', 'MAYOR_QUE', 'MENOR_IGUAL',
        'MAYOR_IGUAL', 'YLOG', 'OLOG', 'NE'
        ] + reserved.values();
    
    
    t_SU = r'\+'
    t_RE = r'-'
    t_MULT = r'\*'
    t_DIV = r'/'
    t_MOD = r'%'
    t_ASIG = r'='
    t_REAL = r'[0-9]+\.[0-9]+'
    t_ENTERO = r'[0-9]+'
    t_ignore_BLANCOS = r'\r|\n|\r\n|[ \t]+'
    t_PAR_AB = r'\('
    t_PAR_CERR = r'\)'
    t_LLAVE_AB = r'{'
    t_LLAVE_CERR = r'}'
    t_IGUAL_IGUAL = r'=='
    t_DISTINTO = r'!='
    t_MENOR_QUE = r'<'
    t_MAYOR_QUE = r'>'
    t_MENOR_IGUAL = r'<='
    t_MAYOR_IGUAL = r'>='
    t_YLOG = r'&&'
    t_OLOG = r'\|\|'
    t_PUNTO_Y_COMA = r';'
      
    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'IDENT')
        return t
    
    def t_COMENT(self, t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')
        
    def t_EOL(self, t):
        ur'\n+'
        t.lexer.lineno += t.value.count("\n")
        
    def t_error(self, t):
        print "Error lexicologico caracter ilegal '%s' en la linea %d" % (t.value[0], t.lexer.lineno)
        self.errorCount = self.errorCount + 1
        t.lexer.skip(1)
    
    def __init__(self, **kwargs):
         self.__lexer = lex.lex(object=self, **kwargs)

    def getLexer(self):
        return self.__lexer
