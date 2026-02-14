#################PROYECTO##################
__proyect__    = "Regex2Excel"
__author__     = "Mario Rubio Avila"
__version__    = "V26.02.014"
'''  
'''
__maintainer__ = "Mario Rubio"
__status__     = "Development" #"Prototype", "Development", or "Production"
__infoAPP__    = "Dado un fichero de texto busca una expresión regular y las coincidencias las guarda en un xlsx. Permite la busqueda dentro de una carpeta"


debugMode = False

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from tkinter import messagebox
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
        self.procesar = tk.Button(text ="Procesar", command = lambda:self.run_process(),state='disabled', width=250)
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
        # Patrón: opcional prefijo con puntos, nombre de función y paréntesis con argumentos (incluye saltos de línea)
        self.entry.insert(0, r'([a-zA-Z1-9_]+[.]){0,}[a-zA-Z1-9_]+\([a-zA-Z0-9_, .":+\[\]()\-\>\n]*\)')


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

    def run_process(self):
        global fileOrigen, fileDestino
        if fileOrigen == '' or fileDestino == '':
            messagebox.showerror(message="Origen o destino no seleccionados.", title="Error")
            return
        try:
            df = self.procesarDocumento(fileOrigen, fileDestino)
        except Exception as e:
            messagebox.showerror(message=f"Error procesando el fichero:\n{e}", title="Error Procesado")
            return
        # Mostrar modal con resultado y opción de abrir fichero
        self.post_process_modal(fileDestino, df)

    def post_process_modal(self, filepath, df):
        # Crear ventana modal personalizada
        modal = tk.Toplevel(self.parent)
        modal.title("Resultado")
        modal.geometry("420x160")
        modal.transient(self.parent)
        modal.grab_set()

        resultados = []
        try:
            resultados = df.get('resultados', [])
            if isinstance(resultados, pd.Series):
                resultados = resultados.tolist()
        except Exception:
            resultados = []

        count = len(resultados) if hasattr(resultados, '__len__') else 0

        lbl = tk.Label(modal, text=f"Procesado. Resultados: {count}\nArchivo: {filepath}", justify=tk.LEFT, wraplength=400)
        lbl.pack(padx=12, pady=12)

        btn_frame = tk.Frame(modal)
        btn_frame.pack(pady=8)

        def open_and_close():
            try:
                if os.name == 'nt':
                    os.startfile(filepath)
                else:
                    # cross-platform fallback
                    import webbrowser
                    webbrowser.open('file://' + os.path.abspath(filepath))
            except Exception as e:
                messagebox.showerror(message=f"No se pudo abrir el fichero:\n{e}", title="Error Abrir")
            modal.destroy()

        def just_close():
            modal.destroy()

        abrir_btn = tk.Button(btn_frame, text="Abrir fichero", command=open_and_close, width=15)
        abrir_btn.pack(side=tk.LEFT, padx=8)
        terminar_btn = tk.Button(btn_frame, text="Terminar", command=just_close, width=15)
        terminar_btn.pack(side=tk.LEFT, padx=8)

        # Center modal over parent
        self.parent.update_idletasks()
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() // 2) - (420 // 2)
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() // 2) - (160 // 2)
        modal.geometry(f"+{x}+{y}")
        modal.wait_window()

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