# Generadores de Números Pseudoaleatorios · 901N

Proyecto de la asignatura **Modelación y Simulación**, Universidad de
Cundinamarca, grupo **901N**.

**Integrantes**
- Kelly Johanna Garzon Becerra — kellyjgarzon@ucundinamarca.edu.co
- Andres Felipe Rodriguez Correa — afrodriguezcorrea@ucundinamarca.edu.co
- Jonathan David Chavarro Segura — jdchavarro@ucundinamarca.edu.co

## Qué hace

Un sitio Flask con una página interactiva por cada método o prueba visto
en clase (contenido basado en *Modelación · Semana 3 y 4*):

**Métodos no congruenciales**
- Cuadrados medios
- Productos medios
- Multiplicador constante

**Métodos congruenciales**
- Congruencial lineal
- Congruencial multiplicativo
- Congruencial aditivo
- Período máximo (teorema de Hull-Dobell)

**Pruebas estadísticas**
- Prueba de medias
- Prueba de varianza
- Prueba Chi-cuadrada (uniformidad)
- Prueba Kolmogorov-Smirnov (uniformidad)
- Prueba de corridas arriba y abajo de la media (independencia)

Cada página explica brevemente el método/prueba, muestra su fórmula y
tiene un formulario a la izquierda con resultados y gráfico a la
derecha. Cuando un método admite varias semillas (productos medios,
congruencial aditivo, período máximo) o un conjunto de datos (las 5
pruebas), el campo acepta valores **separados por coma**.

## Arquitectura

```
app/
  __init__.py            create_app(): registra los 3 blueprints
  config.py               configuración de Flask

  inicio/                 blueprint del home (portada del curso)
    routes.py

  generadores/            blueprint de los métodos de generación
    rutas_directos.py       rutas: cuadrados/productos medios, mult. constante
    rutas_congruenciales.py rutas: lineal, multiplicativo, aditivo, período máx.
    logica/                 funciones puras de cálculo (sin Flask)
      comunes.py
      metodos_directos.py
      metodos_congruenciales.py

  pruebas/                blueprint de las pruebas estadísticas
    routes.py
    logica/                 funciones puras de cálculo (sin Flask)
      comunes.py
      distribuciones.py      normal_ppf, chi2_ppf, ks_valor_critico
      pruebas_estadisticas.py

  templates/
    base.html               layout, navbar y footer compartidos
    macros/                  campos de formulario, panel de resultados,
                             hipótesis/veredicto de las pruebas
    inicio/index.html
    generadores/*.html       7 plantillas, una por método
    pruebas/*.html           5 plantillas, una por prueba

  static/
    css/styles.css
    js/main.js               histograma, exportar CSV, copiar tabla

run.py                    punto de entrada de desarrollo
requirements.txt
```

La idea de separar `logica/` de las rutas es que cada algoritmo se pueda
leer, probar o reutilizar sin depender de Flask: son funciones puras que
reciben números y devuelven listas/diccionarios.

## Instalación y ejecución

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate

pip install -r requirements.txt

python run.py
```

Abre `http://127.0.0.1:5000` en el navegador.

## Notas sobre las fórmulas

- En los métodos **no congruenciales** (cuadrados medios, productos
  medios, multiplicador constante): R<sub>i</sub> = 0.X<sub>i</sub> (los D
  dígitos centrales, interpretados como decimales).
- En los métodos **congruenciales** (lineal, multiplicativo, aditivo,
  período máximo): R<sub>i</sub> = X<sub>i</sub> / (m − 1), tal como lo
  define el documento de clase.
- Las pruebas estadísticas usan aproximaciones numéricas propias (sin
  `scipy`) para los cuantiles de las distribuciones normal y
  Chi-cuadrada, y la fórmula asintótica de Kolmogorov para el valor
  crítico de Kolmogorov-Smirnov. Son suficientemente precisas para fines
  didácticos, pero si tu profesor exige los valores exactos de tabla,
  compáralos contra el anexo del libro guía.
