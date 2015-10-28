import sys
import os
sys.path.insert(0,"../..")

from scparser import Generator

if(__name__ == "__main__"):
    program = ""
    f = None
    if(len(sys.argv) != 3):
       print "Uso: sc archivofuente archivopolaca"
       exit()
    else:
        f = open(sys.argv[1], 'r')
    
    for line in f.readlines(): 
        program = program + line

    #unlink(sys.argv[2])
    gen = Generator()
    gen.run(program)
    errors = gen.getErrors()
    if(errors == 0):
        gen.exportPolaca(sys.argv[2])
    else:
        print "\nError!. No se ha generado la forma interna debido a errores en el codigo fuente.\n"
    f.close()
