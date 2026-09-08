"""Métodos NO congruenciales de generación de números pseudoaleatorios.

Cuadrados medios, productos medios y multiplicador constante, tal como se
describen en "Modelación · Semana 3 y 4" (sección 3, algoritmos no
congruenciales). Cada función es pura: recibe parámetros y devuelve
estructuras de datos simples (listas de diccionarios) listas para pintar
en una tabla Jinja2.
"""

from __future__ import annotations

from .comunes import extraer_medio


def generar_cuadrados_medios(
    semilla: int, cantidad: int, digitos: int | None = None
) -> tuple[list[dict], int, int | None]:
    """Algoritmo de cuadrados medios (Von Neumann / Metropolis, años 40).

    Yi = Xi^2 ; Xi+1 = dígitos centrales de Yi ; Ri = 0.Xi+1
    """
    if digitos is None:
        digitos = len(str(semilla))

    x = semilla
    resultados: list[dict] = []
    vistos: dict[int, int] = {semilla: 0}
    ciclo: int | None = None

    for i in range(1, cantidad + 1):
        cuadrado = x * x
        medio = extraer_medio(cuadrado, digitos)
        x_siguiente = int(medio)
        ri = x_siguiente / (10 ** digitos)

        resultados.append(
            {"i": i, "x": x, "cuadrado": cuadrado, "medio": medio, "xi": x_siguiente, "ri": ri}
        )

        if ciclo is None:
            if x_siguiente in vistos:
                ciclo = i
            else:
                vistos[x_siguiente] = i

        x = x_siguiente

    return resultados, digitos, ciclo


def generar_productos_medios(
    semillas: list[int], cantidad: int, digitos: int | None = None
) -> tuple[list[dict], int]:
    """Algoritmo de productos medios, generalizado a orden k = len(semillas).

    Con k = 2 semillas es el método clásico: Yi = Xi-1 · Xi-2 ; Xi = dígitos
    centrales de Yi. Con más semillas, cada nuevo término multiplica el
    valor más antiguo y el más reciente de la ventana de k semillas.
    """
    if digitos is None:
        digitos = len(str(semillas[0]))

    ventana = list(semillas)
    resultados: list[dict] = []

    for i in range(1, cantidad + 1):
        x_antiguo = ventana[0]
        x_reciente = ventana[-1]
        producto = x_antiguo * x_reciente
        medio = extraer_medio(producto, digitos)
        x_nuevo = int(medio)
        ri = x_nuevo / (10 ** digitos)

        resultados.append(
            {
                "i": i,
                "xa": x_antiguo,
                "xb": x_reciente,
                "producto": producto,
                "medio": medio,
                "xi": x_nuevo,
                "ri": ri,
            }
        )

        ventana = ventana[1:] + [x_nuevo]

    return resultados, digitos


def generar_multiplicador_constante(
    semilla: int, constante: int, cantidad: int, digitos: int | None = None
) -> tuple[list[dict], int]:
    """Algoritmo de multiplicador constante: Yi = a · Xi ; Xi+1 = dígitos
    centrales de Yi ; Ri = 0.Xi+1."""
    if digitos is None:
        digitos = len(str(semilla))

    x = semilla
    resultados: list[dict] = []

    for i in range(1, cantidad + 1):
        producto = constante * x
        medio = extraer_medio(producto, digitos)
        x_siguiente = int(medio)
        ri = x_siguiente / (10 ** digitos)

        resultados.append(
            {"i": i, "x": x, "a": constante, "producto": producto, "medio": medio, "xi": x_siguiente, "ri": ri}
        )

        x = x_siguiente

    return resultados, digitos
