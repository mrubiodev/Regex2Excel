# Changelog

All notable changes to this project are documented in this file.

## [V26.02.014] - 2026-02-14
- Correcciones:
  - Se corrige la captura de coincidencias: ahora se obtienen todas las coincidencias por línea (antes solo la primera).
  - Se corrige el nombre por defecto de salida: ya no incluye extensiones inesperadas y `asksaveasfilename` usa `defaultextension='.xlsx'`.
  - Se elimina el paréntesis extra añadido a cada coincidencia en la salida.
  - Se añade un modal final al terminar el procesamiento que muestra el número de resultados y ofrece abrir el fichero o cerrar la ventana.
  - Se corrige la cadena regex para evitar `SyntaxWarning` por escapes inválidos (se usa raw string donde corresponde).
  - Mejoras en el empaquetado (`empaquetar.bat`): ahora usa `Regex2Excel.py` como entrypoint por defecto, copia `res/metadata.json` a `dist`, incluye EXE y `metadata.json` dentro del ZIP de release y limpia `build`/`dist` tras el empaquetado.
  - Se instalaron `pandas` y `openpyxl` en el entorno virtual del proyecto para que la importación funcione.

## Notas
- Los problemas anteriormente listados como "Bugs conocidos" fueron corregidos en esta versión. Si detectas algún comportamiento inesperado, abre un issue con pasos reproducibles.
