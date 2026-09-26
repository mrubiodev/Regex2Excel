# Regex2Excel

![Estado](https://img.shields.io/badge/estado-En%20desarrollo-yellow)
![Python](https://img.shields.io/badge/Python-GUI-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Interfaz-Tkinter-444444)
![Pandas](https://img.shields.io/badge/Datos-Pandas-150458?logo=pandas&logoColor=white)
![Excel](https://img.shields.io/badge/Salida-XLSX-217346?logo=microsoftexcel&logoColor=white)

Aplicación de escritorio para buscar expresiones regulares en ficheros de texto y exportar las coincidencias a Excel. La versión indicada en el código y en los metadatos es **V26.02.014**.

## Qué hace

- Abre un fichero y busca una expresión regular personalizada.
- Incluye patrones preparados para localizar usos de funciones, llamadas con argumentos y declaraciones de funciones.
- Busca también dentro de una carpeta y sus subcarpetas.
- Exporta a `.xlsx` y muestra al terminar el número de resultados; desde el diálogo final se puede abrir el archivo generado.

En el procesamiento de un único fichero, la aplicación busca en cada línea, recoge todas las coincidencias, elimina duplicados y ordena los resultados. El Excel contiene las columnas `archivo` y `resultados`; no incluye números de línea.

El modo de carpetas recorre los ficheros `.py` y combina los resultados en un único `out_regex.xlsx` en la carpeta de destino.

## Requisitos

- Python y una instalación que incluya Tkinter.
- pandas y openpyxl.

La lista mínima de dependencias para ejecutar la aplicación está en `requirement.txt`:

~~~powershell
python -m pip install -r requirement.txt
~~~

`requirements.txt` contiene el conjunto fijado que usa el empaquetado del proyecto.

## Ejecutar

Desde la raíz del repositorio:

~~~powershell
python Regex2Excel.py
~~~

En la ventana, escribe o selecciona un patrón desde el menú **Archivo**, pulsa **Cargar** para elegir el fichero y **Guardar** para escoger el Excel de salida. Después pulsa **Procesar**.

Los patrones del menú son solo puntos de partida: puedes editar la expresión antes de procesar. En **Buscar En Carpetas**, selecciona la carpeta de origen y la de destino.

## Limitaciones y notas

- Las expresiones se aplican línea por línea; no se buscan coincidencias que abarquen varias líneas.
- En la búsqueda de carpetas, la extensión está fijada a `.py` en el código. Si no encuentra ningún fichero compatible, la combinación de resultados puede fallar.
- `run.bat` todavía intenta abrir un nombre de script antiguo que ya no existe. Usa `python Regex2Excel.py`.
- El ZIP que aparece en `release/` se llama `Regex2Excel_V22.10.0.025.zip`, anterior a la versión actual del código. No lo confundas con una compilación de V26.02.014.
- `CreateEnv.bat` elimina la carpeta `.venv` existente antes de crearla de nuevo. Si quieres conservar un entorno virtual, no uses ese script; crea uno manualmente.

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirement.txt
python Regex2Excel.py
~~~

## Estructura útil

- `Regex2Excel.py`: aplicación y lógica de búsqueda.
- `requirement.txt`: dependencias mínimas para ejecución.
- `requirements.txt`: conjunto fijado para el entorno de empaquetado.
- `res/metadata.json` y `CHANGELOG.md`: metadatos y cambios de la versión.