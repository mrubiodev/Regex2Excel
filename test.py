import re
import pandas as pd

logsInConsole = True
debugMode = False 

fileOrigen  = ""
fileDestino = ""
extensionSalidaBloque ='py'
outFileName = 'out_regex.xlsx'

patron = '([a-zA-Z1-9_]+[.]){0,}+[a-zA-Z1-9_]+[(]'
    
fileOrigenParametro = ""
fileDestinoParametro = ""

def procesarDocumento( fileOrigenParametro, fileDestinoParametro):
    datos = []
    lineaConteo = []
    datosDic = {}
    
    with open(fileOrigenParametro) as fname:
        nombreFichero = fileOrigenParametro.split('/')[-1]
        lineas = fname.readlines()
        contadorLinea = 1
        for linea in lineas:
            regularExpresion = patron
            try:
                #x = re.findall(regularExpresion,linea)
                #p = re.compile(re.escape(regularExpresion))
                #x= p.match(linea.strip('\n'))
                x =linea.find(regularExpresion)
                #x = re.search(regularExpresion, linea.strip('\n'))
                if (x != None and x >= 0):
                    #if (len(x.regs) > 1): print ('Revise la linea : ' + str(contadorLinea))
                    patronAVolcar = x.string[x.regs[0][0]:x.regs[0][1]] + ")"
                    if (logsInConsole and debugMode): print ('Encontrado : ' + str(x.string))
                    if (logsInConsole and debugMode): print ('Patron : '+  patronAVolcar)
                    datos.append(patronAVolcar)
            except Exception as e:
                if (logsInConsole and debugMode): print ('Exception : ' + str(e.string))
            contadorLinea =contadorLinea+1
                
        datosSalida = sorted(set(datos))
        datosDic['archivo']    = nombreFichero
        datosDic['resultados'] = datosSalida
            
        df = pd.DataFrame(datosDic, columns = ['archivo', 'resultados'])
        df.to_excel(fileDestinoParametro, sheet_name='resultados')
        if (logsInConsole): print ('Fichero guardado : '+  fileDestinoParametro)
        return df
    
############################## MAIN ##########################################
if __name__ == "__main__":
    print("-------------------------")
