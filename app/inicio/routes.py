from flask import render_template

from . import bp

# Información del curso y del equipo, centralizada aquí para que la
# plantilla del home no tenga datos "quemados" en el HTML.
CURSO = {
    "nombre": "Modelación y Simulación",
    "universidad": "Universidad de Cundinamarca",
    "grupo": "901N",
}

INTEGRANTES = [
    {
        "nombre": "Kelly Johanna Garzon Becerra",
        "correo": "kellyjgarzon@ucundinamarca.edu.co",
    },
    {
        "nombre": "Andres Felipe Rodriguez Correa",
        "correo": "afrodriguezcorrea@ucundinamarca.edu.co",
    },
    {
        "nombre": "Jonathan David Chavarro Segura",
        "correo": "jdchavarro@ucundinamarca.edu.co",
    },
]

# Temario mostrado en el home a modo de "índice" de lo visto en clase,
# con enlace directo a cada página/generador/prueba correspondiente.
# Cada tema trae ya todo lo necesario para pintar su tarjeta (macro
# tarjeta_metodo en macros/tarjetas.html), agrupado por bloque.
TEMARIO = [
    {
        "bloque": "Métodos no congruenciales",
        "temas": [
            {
                "titulo": "Cuadrados medios",
                "endpoint": "generadores.cuadrados_medios",
                "tag": "Método no congruencial",
                "icono": "bi-fullscreen-exit",
                "descripcion": "Eleva la semilla al cuadrado y extrae los dígitos centrales para obtener el siguiente valor.",
                "formula": "X<sub>i+1</sub> = mitad( X<sub>i</sub><sup>2</sup> )",
                "cta": "Abrir generador",
            },
            {
                "titulo": "Productos medios",
                "endpoint": "generadores.productos_medios",
                "tag": "Método no congruencial",
                "icono": "bi-x-diamond",
                "descripcion": "Multiplica dos semillas consecutivas y toma los dígitos centrales del producto.",
                "formula": "X<sub>i+2</sub> = mitad( X<sub>i</sub> · X<sub>i+1</sub> )",
                "cta": "Abrir generador",
            },
            {
                "titulo": "Multiplicador constante",
                "endpoint": "generadores.multiplicador_constante",
                "tag": "Método no congruencial",
                "icono": "bi-asterisk",
                "descripcion": "Multiplica la semilla por una constante fija y conserva los dígitos centrales del resultado.",
                "formula": "X<sub>i+1</sub> = mitad( a · X<sub>i</sub> )",
                "cta": "Abrir generador",
            },
        ],
    },
    {
        "bloque": "Métodos congruenciales",
        "temas": [
            {
                "titulo": "Congruencial lineal",
                "endpoint": "generadores.congruencial_lineal",
                "tag": "Método congruencial",
                "icono": "bi-arrow-repeat",
                "descripcion": "Combina multiplicador, incremento y módulo en una relación de recurrencia clásica.",
                "formula": "X<sub>i+1</sub> = ( a·X<sub>i</sub> + c ) mod m",
                "cta": "Abrir generador",
            },
            {
                "titulo": "Congruencial multiplicativo",
                "endpoint": "generadores.congruencial_multiplicativo",
                "tag": "Método congruencial",
                "icono": "bi-x-circle",
                "descripcion": "Caso particular del congruencial lineal sin incremento (c = 0): solo semilla y multiplicador.",
                "formula": "X<sub>i+1</sub> = ( a·X<sub>i</sub> ) mod m",
                "cta": "Abrir generador",
            },
            {
                "titulo": "Congruencial aditivo",
                "endpoint": "generadores.congruencial_aditivo",
                "tag": "Método congruencial",
                "icono": "bi-plus-circle",
                "descripcion": "Cada término es la suma módulo m de dos semillas anteriores. Admite orden k generalizado.",
                "formula": "X<sub>i</sub> = ( X<sub>i-1</sub> + X<sub>i-k</sub> ) mod m",
                "cta": "Abrir generador",
            },
            {
                "titulo": "Período máximo (lineal)",
                "endpoint": "generadores.periodo_maximo_congruencial_lineal",
                "tag": "Análisis",
                "icono": "bi-rulers",
                "descripcion": "Evalúa si un congruencial lineal recorre todos los valores posibles antes de repetirse (teorema de Hull-Dobell).",
                "formula": "mcd(c,m)=1 · (a−1) múltiplo de los primos de m",
                "cta": "Abrir análisis",
            },
        ],
    },
    {
        "bloque": "Pruebas estadísticas",
        "temas": [
            {
                "titulo": "Prueba de medias",
                "endpoint": "pruebas.medias",
                "tag": "Prueba estadística",
                "icono": "bi-calculator",
                "descripcion": "Verifica si el promedio del conjunto de R<sub>i</sub> es estadísticamente igual a 0.5.",
                "formula": "H<sub>0</sub>: μ = 0.5",
                "cta": "Abrir prueba",
            },
            {
                "titulo": "Prueba de varianza",
                "endpoint": "pruebas.varianza",
                "tag": "Prueba estadística",
                "icono": "bi-distribute-vertical",
                "descripcion": "Verifica si la varianza del conjunto de R<sub>i</sub> es estadísticamente igual a 1/12.",
                "formula": "H<sub>0</sub>: σ² = 1/12",
                "cta": "Abrir prueba",
            },
            {
                "titulo": "Chi-cuadrada",
                "endpoint": "pruebas.chi_cuadrada",
                "tag": "Prueba de uniformidad",
                "icono": "bi-bar-chart-steps",
                "descripcion": "Compara las frecuencias observadas y esperadas de los R<sub>i</sub> repartidos en m sub-intervalos.",
                "formula": "χ² = Σ (O<sub>i</sub> − E<sub>i</sub>)² / E<sub>i</sub>",
                "cta": "Abrir prueba",
            },
            {
                "titulo": "Kolmogorov-Smirnov",
                "endpoint": "pruebas.kolmogorov_smirnov",
                "tag": "Prueba de uniformidad",
                "icono": "bi-graph-up",
                "descripcion": "Compara la distribución empírica de los R<sub>i</sub> ordenados contra la uniforme teórica. Ideal para n pequeños.",
                "formula": "D = max(D⁺, D⁻)",
                "cta": "Abrir prueba",
            },
            {
                "titulo": "Corridas arriba y abajo",
                "endpoint": "pruebas.corridas",
                "tag": "Prueba de independencia",
                "icono": "bi-shuffle",
                "descripcion": "Cuenta las corridas de 1s y 0s (según R<sub>i</sub> ≷ 0.5) para detectar correlación entre los números.",
                "formula": "Z<sub>0</sub> = (C<sub>0</sub> − μ<sub>C0</sub>) / σ<sub>C0</sub>",
                "cta": "Abrir prueba",
            },
        ],
    },
    {
        "bloque": "Actividad adicional",
        "temas": [
            {
                "titulo": "Comparación de algoritmos",
                "endpoint": "generadores.comparacion",
                "tag": "Congruencial lineal vs. Productos medios",
                "icono": "bi-bar-chart-line",
                "descripcion": "Genera una secuencia en cada uno de los 2 algoritmos elegidos y compara su comportamiento estadístico (uniformidad, media, varianza e independencia) en una sola tabla.",
                "formula": "Uniformidad · Media · Varianza · Independencia",
                "cta": "Ver comparación",
            },
        ],
    },
]


@bp.route("/")
def index():
    return render_template(
        "inicio/index.html",
        curso=CURSO,
        integrantes=INTEGRANTES,
        temario=TEMARIO,
    )
