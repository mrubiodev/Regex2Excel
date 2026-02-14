
Regex2Excel
===========

Descripción
- Herramienta con interfaz gráfica (Tkinter) que busca coincidencias de expresiones regulares en un fichero o en todos los ficheros de una carpeta y exporta los resultados a un archivo Excel (.xlsx).

Características principales
- Interfaz GUI para introducir la expresión regular y seleccionar ficheros/carpetas.
- Menú con atajos: `Info`, `Buscar Uso Funciones`, `Buscar Uso Funciones Y Argumentos`, `Buscar Declaracion Funciones`, `Buscar En Carpetas`, `Exit`.
- Exporta coincidencias a Excel usando `pandas.DataFrame.to_excel()`.

Detalles técnicos
- Punto de entrada: `Regex2Excel.py` (ejecutable como script).  
- Versión embebida en el script: `V22.10.0.025`.
- Dependencias principales: `pandas` y `openpyxl` (para escribir .xlsx).  
- Usa la librería estándar `tkinter` para la interfaz.

Comportamiento de búsqueda y formato de salida
- La app lee el fichero línea a línea y busca la primera coincidencia por línea (no devuelve múltiples coincidencias en la misma línea).  
- Al volcar la coincidencia, el código añade un paréntesis de cierre ")" al final de cada resultado.  
- Al procesar carpetas, filtra ficheros por la extensión marcada en la variable `extensionSalidaBloque` (por defecto `py`) y concatena los resultados en `out_regex.xlsx` salvo que se indique otro destino.

Instalación
1. Crear entorno (opcional): ejecutar `CreateEnv.bat`.  
2. Instalar dependencias:

```powershell
pip install -r requirement.txt
```

Ejecución
- Ejecutar GUI:

```powershell
run.bat
# o
python Regex2Excel.py
```

- Pasos rápidos en la GUI:
	- Insertar o seleccionar la expresión regular en la caja de texto.
	- Pulsar `Cargar` para elegir el fichero origen (o `Buscar En Carpetas` para procesar una carpeta).
	- Pulsar `Guardar` para seleccionar fichero de salida `.xlsx`.
	- Pulsar `Procesar` para generar el Excel con los resultados.

Archivos relevantes
- `Regex2Excel.py` — script principal con la interfaz y la lógica.  
- `requirement.txt` — lista de dependencias (nota: se llama `requirement.txt` en este repositorio).
- `res/metadata.json` — metadatos del proyecto actualizados.

Problemas conocidos (resueltos)
- Si la expresión aparece más de una vez en la misma línea, sólo se capturaba la primera coincidencia. (Resuelto: ahora se capturan todas las coincidencias por línea.)
- El nombre de salida por defecto podía incluir la extensión `.xml` y provocar errores al guardar. (Resuelto: el nombre por defecto ahora se calcula sin extensión y `defaultextension` es `.xlsx`.)
- Las coincidencias volcadas terminaban con un paréntesis `)` añadido por el código. (Resuelto: ya no se añade el paréntesis adicional.)

Sugerencias / próximos pasos
- Renombrar `requirement.txt` a `requirements.txt` para compatibilidad estándar.  
- Añadir un comprobador para capturar múltiples coincidencias por línea si se desea ese comportamiento.  
- Quitar la adición automática de `)` a la salida o documentarlo explícitamente.

Contacto
- Autor: Mario Rubio Avila

SEARCH_REGULAR_EXPRESION_IN_FILE_TO_XLSX
