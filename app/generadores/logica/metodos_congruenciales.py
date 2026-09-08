"""Métodos congruenciales de generación de números pseudoaleatorios.

Lineal, multiplicativo, aditivo y el análisis de período máximo
(teorema de Hull-Dobell), tal como se describen en "Modelación · Semana 3
y 4" (sección 3). En los tres métodos, una vez calculado el entero Xi, el
número pseudoaleatorio real se obtiene con Ri = Xi / (m - 1).
"""

from __future__ import annotations

from math import gcd

from .comunes import factores_primos


def _ri(xi: int, m: int) -> float:
    return xi / (m - 1) if m > 1 else 0.0


def generar_congruencial_lineal(x0: int, a: int, c: int, m: int, cantidad: int) -> list[dict]:
    """Xi+1 = (a·Xi + c) mod m ; Ri = Xi / (m - 1)."""
    x = x0
    resultados: list[dict] = []
    for i in range(1, cantidad + 1):
        x = (a * x + c) % m
        resultados.append({"i": i, "xi": x, "ri": _ri(x, m)})
    return resultados


def generar_congruencial_multiplicativo(x0: int, a: int, m: int, cantidad: int) -> list[dict]:
    """Caso particular del lineal con c = 0: Xi+1 = (a·Xi) mod m."""
    x = x0
    resultados: list[dict] = []
    for i in range(1, cantidad + 1):
        x = (a * x) % m
        resultados.append({"i": i, "xi": x, "ri": _ri(x, m)})
    return resultados


def generar_congruencial_aditivo(semillas: list[int], m: int, cantidad: int) -> list[dict]:
    """Xi = (Xi-1 + Xi-k) mod m, con k = número de semillas iniciales."""
    ventana = list(semillas)
    resultados: list[dict] = []
    for i in range(1, cantidad + 1):
        x_antiguo = ventana[0]      # Xi-k
        x_reciente = ventana[-1]    # Xi-1
        xi = (x_reciente + x_antiguo) % m
        resultados.append({"i": i, "xa": x_antiguo, "xb": x_reciente, "xi": xi, "ri": _ri(xi, m)})
        ventana = ventana[1:] + [xi]
    return resultados


def evaluar_hull_dobell(a: int, c: int, m: int) -> dict:
    """Condiciones de Banks, Carson, Nelson y Nicol para que un congruencial
    lineal alcance su período máximo N = m, sin importar la semilla X0:

    1) mcd(c, m) = 1
    2) (a - 1) es divisible por cada primo que divide a m
    3) si m es múltiplo de 4, entonces (a - 1) también es múltiplo de 4
    """
    primos_m = factores_primos(m)
    cond1 = gcd(c, m) == 1
    cond2 = all((a - 1) % p == 0 for p in primos_m) if primos_m else True
    cond3_aplica = m % 4 == 0
    cond3 = ((a - 1) % 4 == 0) if cond3_aplica else True

    return {
        "cond1_cm_coprimos": cond1,
        "cond2_a1_divisible_primos": cond2,
        "cond3_a1_divisible_4": cond3,
        "cond3_aplica": cond3_aplica,
        "primos_m": primos_m,
        "cumple_periodo_maximo": cond1 and cond2 and cond3,
    }


def generar_secuencia_con_periodo(
    x0: int, a: int, c: int, m: int, limite: int
) -> tuple[list[dict], int | None, int | None]:
    """Genera un congruencial lineal hasta que un valor de Xi se repite (o
    hasta `limite` términos, como tope de seguridad para módulos grandes).

    Devuelve (resultados, periodo, inicio_ciclo):
      - periodo: cantidad de términos que dura el ciclo detectado.
      - inicio_ciclo: índice del primer término del ciclo (0 si el ciclo
        vuelve exactamente a la semilla X0, mayor que 0 si el generador
        "cae" en un ciclo distinto sin pasar de nuevo por X0).
    """
    vistos = {x0: 0}
    x = x0
    resultados: list[dict] = []
    periodo = None
    inicio_ciclo = None

    for i in range(1, limite + 1):
        x = (a * x + c) % m
        resultados.append({"i": i, "xi": x, "ri": _ri(x, m)})
        if x in vistos:
            inicio_ciclo = vistos[x]
            periodo = i - inicio_ciclo
            break
        vistos[x] = i

    return resultados, periodo, inicio_ciclo
