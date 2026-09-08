"""Pruebas estadísticas para números pseudoaleatorios (sección 5 de
"Modelación · Semana 3 y 4"): medias, varianza, uniformidad
(Chi-cuadrada y Kolmogorov-Smirnov) e independencia (corridas arriba y
abajo de la media).

Cada función recibe el conjunto de números Ri y el nivel de significancia
α, y devuelve un diccionario con los cálculos intermedios y el veredicto
(se rechaza o no se rechaza H0), listo para pintar en la plantilla.
"""

from __future__ import annotations

import math

from .distribuciones import chi2_ppf, ks_valor_critico, normal_ppf


def prueba_medias(valores: list[float], alpha: float = 0.05) -> dict:
    """H0: la media de los Ri es 0.5.  H1: la media no es 0.5."""
    n = len(valores)
    r_barra = sum(valores) / n
    z = normal_ppf(1 - alpha / 2)
    margen = z * (1 / math.sqrt(12 * n))
    li, ls = 0.5 - margen, 0.5 + margen
    cumple = li <= r_barra <= ls

    return {
        "n": n, "r_barra": r_barra, "alpha": alpha, "z": z,
        "li": li, "ls": ls, "cumple": cumple,
    }


def prueba_varianza(valores: list[float], alpha: float = 0.05) -> dict:
    """H0: la varianza de los Ri es 1/12.  H1: la varianza no es 1/12."""
    n = len(valores)
    r_barra = sum(valores) / n
    varianza = sum((r - r_barra) ** 2 for r in valores) / (n - 1)

    chi2_inf = chi2_ppf(alpha / 2, n - 1)
    chi2_sup = chi2_ppf(1 - alpha / 2, n - 1)
    li = chi2_inf / (12 * (n - 1))
    ls = chi2_sup / (12 * (n - 1))
    cumple = li <= varianza <= ls

    return {
        "n": n, "r_barra": r_barra, "varianza": varianza, "alpha": alpha,
        "chi2_inf": chi2_inf, "chi2_sup": chi2_sup, "li": li, "ls": ls, "cumple": cumple,
    }


def prueba_chi_cuadrada(valores: list[float], alpha: float = 0.05, m: int | None = None) -> dict:
    """H0: los Ri se distribuyen U(0,1).  H1: no se distribuyen U(0,1).

    Divide (0,1) en m sub-intervalos (m = round(sqrt(n)) por defecto) y
    compara frecuencias observadas vs. esperadas con el estadístico χ².
    """
    n = len(valores)
    m = m or max(2, round(math.sqrt(n)))

    frecuencias = [0] * m
    for r in valores:
        idx = int(r * m)
        if idx >= m:
            idx = m - 1
        frecuencias[idx] += 1

    esperada = n / m
    intervalos = []
    chi2_calculado = 0.0
    for i, oi in enumerate(frecuencias):
        aporte = (oi - esperada) ** 2 / esperada
        chi2_calculado += aporte
        intervalos.append({
            "limite_inf": i / m, "limite_sup": (i + 1) / m,
            "oi": oi, "ei": esperada, "aporte": aporte,
        })

    chi2_critico = chi2_ppf(1 - alpha, m - 1)
    cumple = chi2_calculado <= chi2_critico

    return {
        "n": n, "m": m, "alpha": alpha, "intervalos": intervalos,
        "chi2_calculado": chi2_calculado, "chi2_critico": chi2_critico, "cumple": cumple,
    }


def prueba_kolmogorov_smirnov(valores: list[float], alpha: float = 0.05) -> dict:
    """H0: los Ri se distribuyen U(0,1).  H1: no se distribuyen U(0,1).

    Compara la función de distribución empírica F(r) = i/n contra la
    distribución uniforme teórica, para el conjunto ordenado de Ri.
    """
    n = len(valores)
    ordenados = sorted(valores)

    d_mas = max((i / n) - r for i, r in enumerate(ordenados, start=1))
    d_menos = max(r - ((i - 1) / n) for i, r in enumerate(ordenados, start=1))
    d = max(d_mas, d_menos)

    d_critico = ks_valor_critico(alpha, n)
    cumple = d <= d_critico

    filas = [
        {"i": i, "ri": r, "i_n": i / n, "i1_n": (i - 1) / n}
        for i, r in enumerate(ordenados, start=1)
    ]

    return {
        "n": n, "alpha": alpha, "ordenados": ordenados, "filas": filas,
        "d_mas": d_mas, "d_menos": d_menos, "d": d, "d_critico": d_critico, "cumple": cumple,
    }


def prueba_corridas(valores: list[float], alpha: float = 0.05) -> dict:
    """H0: los Ri son independientes.  H1: los Ri no son independientes.

    Prueba de corridas arriba y abajo de la media: construye una secuencia
    de 1 (Ri ≥ 0.5) y 0 (Ri < 0.5), cuenta el número de corridas C0 y lo
    compara contra su valor esperado bajo independencia.
    """
    n = len(valores)
    secuencia = [1 if r >= 0.5 else 0 for r in valores]

    c0 = 1
    for i in range(1, n):
        if secuencia[i] != secuencia[i - 1]:
            c0 += 1

    n0 = secuencia.count(0)
    n1 = secuencia.count(1)

    mu_c0 = (2 * n0 * n1) / n + 0.5
    var_c0 = (2 * n0 * n1 * (2 * n0 * n1 - n)) / (n ** 2 * (n - 1))
    z0 = (c0 - mu_c0) / math.sqrt(var_c0) if var_c0 > 0 else 0.0

    z_critico = normal_ppf(1 - alpha / 2)
    cumple = -z_critico <= z0 <= z_critico

    return {
        "n": n, "alpha": alpha, "secuencia": secuencia, "n0": n0, "n1": n1,
        "c0": c0, "mu_c0": mu_c0, "var_c0": var_c0, "z0": z0,
        "z_critico": z_critico, "cumple": cumple,
    }
