"""Comparación estadística entre los 2 algoritmos seleccionados para la
actividad adicional (congruencial lineal y productos medios).

Este módulo no depende de Flask: `resumen_ligero` recibe el dict completo
de `validar_secuencia` y devuelve solo los escalares necesarios para la
tabla comparativa (apto para guardarse en la sesión de Flask, que viaja
en una cookie firmada con límite de tamaño, sin arrastrar las listas
completas de Ri, intervalos o filas). `comparar` arma la tabla y decide
qué algoritmo tuvo mejor comportamiento estadístico.
"""

from __future__ import annotations


def resumen_ligero(validacion: dict, parametros: dict, nombre: str) -> dict:
    """Extrae de `validacion` (el dict que devuelve `validar_secuencia`)
    solo los campos escalares necesarios para comparar, junto con los
    parámetros de generación usados y el nombre del algoritmo."""
    return {
        "nombre": nombre,
        "parametros": parametros,
        "n": validacion["n"],
        "alpha": validacion["alpha"],
        "pasa_todas": validacion["pasa_todas"],
        "uniformidad_cumple": validacion["uniformidad_cumple"],
        "medias": {
            "r_barra": validacion["medias"]["r_barra"],
            "cumple": validacion["medias"]["cumple"],
        },
        "varianza": {
            "varianza": validacion["varianza"]["varianza"],
            "cumple": validacion["varianza"]["cumple"],
        },
        "chi_cuadrada": {
            "chi2_calculado": validacion["chi_cuadrada"]["chi2_calculado"],
            "chi2_critico": validacion["chi_cuadrada"]["chi2_critico"],
            "cumple": validacion["chi_cuadrada"]["cumple"],
        },
        "kolmogorov_smirnov": {
            "d": validacion["kolmogorov_smirnov"]["d"],
            "d_critico": validacion["kolmogorov_smirnov"]["d_critico"],
            "cumple": validacion["kolmogorov_smirnov"]["cumple"],
        },
        "corridas": {
            "z0": validacion["corridas"]["z0"],
            "z_critico": validacion["corridas"]["z_critico"],
            "cumple": validacion["corridas"]["cumple"],
        },
    }


def comparar(comp_lineal: dict | None, comp_productos: dict | None) -> dict | None:
    """Arma la tabla comparativa (propiedad evaluada x algoritmo) y decide
    cuál algoritmo tuvo mejor comportamiento estadístico. Devuelve None si
    todavía falta la validación de alguno de los 2 algoritmos (el usuario
    no ha generado una muestra válida -n >= 30- en esa página)."""
    if not comp_lineal or not comp_productos:
        return None

    filas = [
        {
            "propiedad": "Uniformidad (Chi² y Kolmogorov-Smirnov)",
            "lineal": comp_lineal["uniformidad_cumple"],
            "productos": comp_productos["uniformidad_cumple"],
        },
        {
            "propiedad": "Media",
            "lineal": comp_lineal["medias"]["cumple"],
            "productos": comp_productos["medias"]["cumple"],
        },
        {
            "propiedad": "Varianza",
            "lineal": comp_lineal["varianza"]["cumple"],
            "productos": comp_productos["varianza"]["cumple"],
        },
        {
            "propiedad": "Independencia (corridas)",
            "lineal": comp_lineal["corridas"]["cumple"],
            "productos": comp_productos["corridas"]["cumple"],
        },
    ]

    puntaje_lineal = sum(1 for f in filas if f["lineal"])
    puntaje_productos = sum(1 for f in filas if f["productos"])

    if comp_lineal["pasa_todas"] and comp_productos["pasa_todas"]:
        mejor = "empate_pasan"
    elif puntaje_lineal > puntaje_productos:
        mejor = "lineal"
    elif puntaje_productos > puntaje_lineal:
        mejor = "productos"
    else:
        mejor = "empate_parcial"

    return {
        "filas": filas,
        "puntaje_lineal": puntaje_lineal,
        "puntaje_productos": puntaje_productos,
        "mejor": mejor,
    }
