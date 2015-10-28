# -----------------------------------------------------------------------------
# scparser.py
# Analizador sintactico -- Genera Notacion Polaca Extendida
# para sc (pseudo - c)
# autor Carlos Castellanos Vera
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")
import re
import ply.yacc as yacc
from sclex import Scanner
import parsetab

class Generator(object):
    __scanner = None
    __parser = None
    tokens = []
    polaca = []
    errorCount = 0
    
    __sem = []
    __t = 0
    
    precedence = (
        ('left', 'SU', 'RE'),
        ('left', 'MOD', 'MULT', 'DIV'),
        ('right', 'NE') 
        )
    
    def __init__(self, **kwargs):
        self.__scanner = Scanner()
        self.tokens = self.__scanner.tokens
        self.__parser = yacc.yacc(module=self, **kwargs)

    def run(self, data):
        self.__parser.parse(data)
    
    def getErrors(self):
        return self.__scanner.errorCount + self.errorCount
    
    #Reglas de Produccion
    def p_Program(self, p):
        """Program : ListSent"""
        pass

    def p_ListSent(self, p):
        """ListSent : Sent"""
        pass
    
    def p_ListSent_R(self, p):
        "ListSent : ListSent Sent"
        pass
    
    def p_Sent(self, p):
        """Sent : SentAsig
                | SentIf
                | SentWhile
                | SentFor"""
        pass
    
    def p_SentRead(self, p):
        """Sent : READ PAR_AB IDENT PAR_CERR PUNTO_Y_COMA"""            
        self.polaca.append("CARGADIR")
        self.polaca.append("DIR " + p[3])
        self.polaca.append("READ")
        
    def p_SentWrite(self, p):
        """Sent : WRITE PAR_AB Expresion PAR_CERR PUNTO_Y_COMA"""
        self.polaca.append("WRITE")

    
    def p_SentAsig(self, p):
        """SentAsig : ParteDir ASIG Expresion PUNTO_Y_COMA"""
        self.polaca.append(p[2])

    def p_ParteDir(self, p):
        """ParteDir : IDENT"""
        self.polaca.append("CARGADIR")
        self.polaca.append("DIR " + p[1])

    def p_SentAsig(self, p):
        """SentAsig : ParteDir ASIG Expresion PUNTO_Y_COMA"""
        self.polaca.append(p[2])

    def p_SentAsig2(self, p):
        """SentAsig2 : ParteDir ASIG Expresion"""
        self.polaca.append(p[2])
        
    #IF
    def p_SentIf(self, p):
        """SentIf : ParteIf SentVIf ELSE LLAVE_AB SentVElse LLAVE_CERR"""
        pass
            
    def p_SentIf2(self, p):
        """SentIf : ParteIf SentVIf2"""
        pass        
    
    def p_ParteIf(self, p):
        """ParteIf : IF PAR_AB Cond PAR_CERR LLAVE_AB"""
        self.polaca.append("SSF")
        self.polaca.append("_")
        self.__sem.append(len(self.polaca) - 1)
    
    def p_SentVIf(self, p):
        """SentVIf : ListSent LLAVE_CERR"""
        self.polaca.append("SI")
        self.polaca.append("_")
        self.__sem.append(len(self.polaca) - 1)
        #resolver el ssf para el else
        self.polaca[self.__sem.pop(len(self.__sem) - 2)] = len(self.polaca)
        
    
    def p_SentVIf2(self, p):
        """SentVIf2 : ListSent LLAVE_CERR"""
        self.polaca[self.__sem.pop()] = len(self.polaca)
        
         
    def p_SentVElse(self, p):
        """SentVElse : ListSent"""
        self.polaca[self.__sem.pop()] = len(self.polaca)
         
    
    #FOR
    def p_SentFor(self, p):
        """SentFor : ParteIniFor ParteSentIncF LSentFor LLAVE_CERR"""
        pass
    
    def p_ParteIniFor(self, p):
        """ParteIniFor : SeccionIni Cond PUNTO_Y_COMA"""
        self.polaca.append("SSF")
        self.polaca.append("_")
        self.__sem.append(len(self.polaca) - 1)
        
        self.polaca.append("SI")
        self.polaca.append("_")
        self.__sem.append(len(self.polaca) - 1)

        #SI a r(<inc>)
        self.__sem.append(len(self.polaca))

    def p_SeccionIni(self, p):
        """SeccionIni : FOR PAR_AB SentAsig2 PUNTO_Y_COMA"""
        self.__sem.append(len(self.polaca))        
        
    
    def p_ParteSentIncF(self, p):
        """ParteSentIncF : SentAsig2 PAR_CERR LLAVE_AB"""
        self.polaca.append("SI")
        self.polaca.append(self.__sem.pop(len(self.__sem) - 4)) #salto para condicion
        self.polaca[self.__sem.pop(len(self.__sem) - 2)] = len(self.polaca)

    def p_LSentFor(self, p):
        """LSentFor : ListSent"""
        self.polaca.append("SI")
        self.polaca.append(self.__sem.pop())
        self.polaca[self.__sem.pop()] = len(self.polaca)
    
    #WHILE
    def p_SentWhile(self, p):
        """SentWhile : ParteWhile ParteSentW LLAVE_CERR"""
        pass
    
    def p_ParteWhile(self, p):
        """ParteWhile : WhileParAb Cond PAR_CERR LLAVE_AB"""
        #self.__sem.append(len(self.polaca) - 1)        
        self.polaca.append("SSF")
        self.polaca.append("_")
        self.__sem.append(len(self.polaca) - 1)

    def p_WhileParAb(self, p):
        """WhileParAb : WHILE PAR_AB"""
        #guardar la dir del comienzo para el si
        self.__sem.append(len(self.polaca))
    
    def p_ParteSentW(self, p):
        """ParteSentW : ListSent"""
        self.polaca.append("SI")
        self.polaca.append("_") #simbolico
        self.polaca[len(self.polaca) - 1] = self.__sem.pop(len(self.__sem) - 2)
        #resolver el SSF
        self.polaca[self.__sem.pop()] = len(self.polaca)
    
    
    def p_Expresion(self, p):
        """Expresion : Expresion SU Expresion
                    | Expresion RE Expresion
                    | Expresion MULT Expresion
                    | Expresion DIV Expresion
                    | Expresion MOD Expresion"""
        self.polaca.append(p[2])
    
    def p_Expresion_IDENT(self, p):
        """Expresion : IDENT"""
        self.polaca.append("CARGA")
        self.polaca.append("DIR " + p[1])        
    
    def p_Expresion_CTE(self, p):
        """Expresion : Constante"""
        pass
    
    def p_Expresion_Group(self, p):
        """Expresion : PAR_AB Expresion PAR_CERR"""
        pass
        
    def p_Expresion_NE(self, p):
        """Expresion : RE Expresion %prec NE"""
        self.polaca.append("NE")
        pass


    def p_Cond(self, p):
        """Cond : Expresion MENOR_IGUAL Expresion
                | Expresion MENOR_QUE  Expresion
                | Expresion MAYOR_IGUAL Expresion
                | Expresion MAYOR_QUE  Expresion
                | Expresion IGUAL_IGUAL Expresion
                | Expresion DISTINTO Expresion"""
        self.polaca.append(p[2])
    
    def p_Cond_Expresion(self, p):
        """Cond : Expresion"""
        pass
        
    def p_Cond_Logic(self, p):
        """Cond : Cond YLOG Cond
                | Cond OLOG Cond"""        
        self.polaca.append(p[2])
    
    def p_Constante(self, p):
        """Constante : TBOOLEAN
                    | FBOOLEAN
                    | ENTERO
                    | REAL"""
        self.polaca.append("CARGADIR")
        self.polaca.append("DIR " + p[1])
               
    #Fin de las reglas de produccion
        
    def p_error(self, p):
        self.errorCount = self.errorCount + 1
        #yacc.errok()
        
    
    def exportPolaca(self, filename):
        f = open(filename, "w")
        i = 0;
        for el in self.polaca:
            try:
                f.write(el + ",")
            except TypeError:
                f.write("%s," % el)
        f.close()
