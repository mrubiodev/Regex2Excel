#################PROYECTO##################
__proyect__    = "Regex2Excel"
__author__     = "Mario Rubio Avila"
__version__    = "V22.10.0.025"
'''  
'''
__maintainer__ = "Mario Rubio"
__status__     = "Development" #"Prototype", "Development", or "Production"
__infoAPP__    = "Dado un fichero de texto busca una expresión regular y las coincidencias las guarda en un xlsx. Permite la busqueda dentro de una carpeta"
'''
Bugs conocidos : 
    Si la expresion aparece más de una vez en la misma linea.Solo coge la primera.
    El nombre de salida por defecto te pone fichero con extension .xml y si no lo borras falla.
'''

debugMode = False

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from tkinter.simpledialog import askstring
from tkinter import messagebox
import xml.etree.ElementTree as ET
import os
import re
import pandas as pd
from datetime import datetime

logsInConsole = True
debugMode = False 

fileOrigen  = ""
fileDestino = ""
extensionSalidaBloque ='py'
outFileName = 'out_regex.xlsx'

REGEX_BUSCAR_FUNCION = r'([a-zA-Z1-9_]+[.]){0,}[a-zA-Z1-9_]+[.][a-zA-Z]+[(]'


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        frame = tk.Frame.__init__(self, parent, *args, **kwargs)
        # Crear el menu principal
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Info",                              command=lambda:self.infoAPP())
        filemenu.add_separator()
        filemenu.add_command(label="Buscar Uso Funciones",              command=lambda:self.setExpresionBuscaFunciones())
        filemenu.add_command(label="Buscar Uso Funciones Y Argumentos", command=lambda:self.setExpresionBuscaFuncionesYArgumentos())
        filemenu.add_command(label="Buscar Declaracion Funciones",      command=lambda:self.setExpresionDeclaracionDeFunciones())
        filemenu.add_separator()
        filemenu.add_command(label="Buscar En Carpetas",                command=lambda:self.modificacionBloque())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="Archivo", menu=filemenu)
        parent.config(menu=menubar)

        self.parent = parent
        self.parent.title("TOOLS - " + __proyect__ + " - " + __version__)
        self.parent.geometry("450x250")
        self.labelOrigen = tk.Label(self.parent, text='Expresion Regular A Buscar', relief=tk.RAISED, width=250 )
        self.labelOrigen.pack(padx = 20, pady=5)
        self.entry = tk.Entry(self.parent, relief=tk.RAISED, width=250 )
        self.entry.pack(padx = 20, pady=10)
        self.cargarBoton = tk.Button(text ="Cargar", command = lambda:self.defineOrigenFile(), width=250)
        self.cargarBoton.pack(padx = 20, pady=0)
        self.labelOrigen = tk.Label(self.parent, text='Origen  : ' + 'No seleccionado', relief=tk.RAISED, width=250 )
        self.labelOrigen.pack(padx = 20, pady=10)
        self.guardarBoton = tk.Button(text ="Guardar", command = lambda:self.defineSalidaFile(),state='disabled', width=250)
        self.guardarBoton.pack(padx = 20, pady=0)
        self.labelDestino = tk.Label(self.parent, text='Destino : ' + 'No seleccionado', relief=tk.RAISED, width=250 )
        self.labelDestino.pack(padx = 20, pady=10)
        self.procesar = tk.Button(text ="Procesar", command = lambda:self.procesarDocumento(fileOrigen,fileDestino),state='disabled', width=250)
        self.procesar.pack(padx = 20, pady=0)

    def infoAPP(self):
        messagebox.showinfo(message=__infoAPP__, title="InfoAPP")

    def setExpresionBuscaFunciones(self):
        self.entry.delete(0,tk.END)
        #Es la expresion regular para buscar llamadas a funciones
        #self.entry.insert(0,'([a-zA-Z1-9_]+[.]){0,}[a-zA-Z1-9_]+[.][a-zA-Z]+[(]') #OLD
        self.entry.insert(0,REGEX_BUSCAR_FUNCION)

    def setExpresionBuscaFuncionesYArgumentos(self):
        self.entry.delete(0,tk.END)
        #Es la expresion regular para buscar llamadas a funciones
        self.entry.insert(0,'([a-zA-Z1-9_]+[.]){0,}+[a-zA-Z1-9_]+[(]+[a-zA-Z0-9_, .":+\[\]()->\n]*)')


    def setExpresionDeclaracionDeFunciones(self):
        self.entry.delete(0,tk.END)
        #Es la expresion regular declaracion de funciones
        self.entry.insert(0,'def [a-zA-Z]+[(]')

    def procesarDocumento(self, fileOrigenParametro, fileDestinoParametro, individualOutputFile = True):
        datos = []
        lineaConteo = []
        datosDic = {}
        with open(fileOrigenParametro, encoding="utf8") as fname:
            nombreFichero = os.path.basename(fileOrigenParametro)
            lineas = fname.readlines()
            contadorLinea = 1
            regularExpresion = self.entry.get()
            try:
                regex = re.compile(regularExpresion)
            except re.error:
                messagebox.showerror(message="Expresión regular inválida.", title="Error Regex")
                return pd.DataFrame({'archivo': [nombreFichero], 'resultados': [[]]})

            for linea in lineas:
                texto_linea = linea.rstrip('\n')
                # Buscar todas las coincidencias en la línea
                for match in regex.finditer(texto_linea):
                    patronAVolcar = match.group(0)
                    if (logsInConsole and debugMode): print ('Encontrado : ' + str(texto_linea))
                    if (logsInConsole and debugMode): print ('Patron : '+  patronAVolcar)
                    datos.append(patronAVolcar)
                contadorLinea = contadorLinea + 1

            datosSalida = sorted(set(datos))
            datosDic['archivo']    = nombreFichero
            datosDic['resultados'] = datosSalida
                
            df = pd.DataFrame(datosDic, columns = ['archivo', 'resultados'])
            if (individualOutputFile): df.to_excel(fileDestinoParametro, sheet_name='resultados')
            if (logsInConsole): print ('Fichero guardado : '+  fileDestinoParametro)
            return df

    def defineOrigenFile(self):
        global fileOrigen
        fileOrigen = askopenfilename(filetypes=[("Todos los ficheros", "*.*")])
        if not (fileOrigen == ''):
            self.labelOrigen.config (text='Origen  : ' + fileOrigen)
            self.guardarBoton.config(state='normal')
        else:
            self.guardarBoton.config(state='disabled')
        self.evaluateActivate()

    def defineSalidaFile(self):
        global fileDestino
        now = datetime.now()
        nameDefault = now.strftime('%Y%m%d_%H%M%S')
        if not (fileOrigen == ''):
            nameDefault = os.path.splitext(os.path.basename(fileOrigen))[0]
        fileDestino = asksaveasfilename(defaultextension='.xlsx', initialfile = nameDefault , filetypes=[("Fichero Excel", "*.xlsx")])
        if not (fileDestino == ''):
            self.labelDestino.config (text='Destino  : ' + fileDestino)
            
        else:
            self.procesar.config(state='disabled')
        self.evaluateActivate()

    def evaluateActivate(self):
        if not (fileOrigen == '') and not (fileDestino == ''):
            self.procesar.config(state='active')

    def modificacionBloque(self):
        carpetaOrigen = askdirectory()
        if (self.entry.get() != ''):
            if not (carpetaOrigen == ''):
                carpetaDestino = askdirectory()
                if not (carpetaDestino == ''):
                    #contenido = os.listdir(carpetaOrigen)
                    listaDic = []
                    for nombre_directorio, dirs, ficheros in os.walk(carpetaOrigen):
                        for nombre_fichero in ficheros:
                            #for documento in contenido:
                            if (nombre_fichero.split('.')[-1] == extensionSalidaBloque):
                                listaDic.append(self.procesarDocumento(nombre_directorio + '\\' + nombre_fichero, carpetaOrigen + '/' + nombre_fichero.split('.')[0] + ".xlsx", False))

                    join = pd.concat(listaDic)   
                    join.to_excel(carpetaDestino + '/' + outFileName, sheet_name='resultados')
                else:
                    messagebox.showerror(message="Se necesita carpeta destino.", title="Error Carpeta")
            else:
                messagebox.showerror(message="Se necesita carpeta a buscar.", title="Error Carpeta")
        else:
            messagebox.showerror(message="Se necesita una expresion regular a buscar.", title="Error Expresion Regular")
                

############################## MAIN ##########################################
if __name__ == "__main__":
    print("-------------------------")
    print("****** "+__proyect__+"  ******")
    print("****** "+__version__+"  ******")
    print("-------------------------")
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=False)
    root.mainloop()
    
else:
    print("El modulo "+ __proyect__ +" sido importado")