"""Validación estadística automática para los 2 algoritmos seleccionados
de la actividad adicional (congruencial lineal y productos medios).

Corre las 5 pruebas (medias, varianza, Chi-cuadrada, Kolmogorov-Smirnov y
corridas) sobre la secuencia de Ri recién generada y arma un resumen con
el veredicto de cada una y si el algoritmo "pasa" en conjunto.

Chi-cuadrada y Kolmogorov-Smirnov son las 2 pruebas de uniformidad: se
corren ambas para tener 2 fuentes de evidencia independientes sobre la
misma hipótesis (Ri ~ U(0,1)), en lugar de apoyarse en una sola.

Depende de `app.pruebas.logica.pruebas_estadisticas`, que son funciones
puras (sin Flask), así que importarlas aquí no crea una dependencia
circular ni acopla los blueprints entre sí.
"""

from __future__ import annotations

from app.pruebas.logica.pruebas_estadisticas import (
    prueba_medias,
    prueba_varianza,
    prueba_chi_cuadrada,
    prueba_kolmogorov_smirnov,
    prueba_corridas,
)

# Con menos datos que esto, las pruebas (sobre todo Chi-cuadrada y
# corridas) dejan de ser confiables, así que la validación automática no
# se ejecuta y se le pide al usuario generar una muestra más grande.
MINIMO_RECOMENDADO = 30


def validar_secuencia(valores_ri: list[float], alpha: float = 0.05) -> dict | None:
    """Corre las 5 pruebas sobre `valores_ri` y devuelve un resumen, o
    None si la muestra es demasiado pequeña para que el resultado sea
    confiable."""
    if len(valores_ri) < MINIMO_RECOMENDADO:
        return None

    medias = prueba_medias(valores_ri, alpha)
    varianza = prueba_varianza(valores_ri, alpha)
    chi_cuadrada = prueba_chi_cuadrada(valores_ri, alpha)
    kolmogorov_smirnov = prueba_kolmogorov_smirnov(valores_ri, alpha)
    corridas = prueba_corridas(valores_ri, alpha)

    uniformidad_cumple = chi_cuadrada["cumple"] and kolmogorov_smirnov["cumple"]

    return {
        "alpha": alpha,
        "n": len(valores_ri),
        "medias": medias,
        "varianza": varianza,
        "chi_cuadrada": chi_cuadrada,
        "kolmogorov_smirnov": kolmogorov_smirnov,
        "corridas": corridas,
        "uniformidad_cumple": uniformidad_cumple,
        "pasa_todas": (
            medias["cumple"] and varianza["cumple"]
            and uniformidad_cumple and corridas["cumple"]
        ),
    }
