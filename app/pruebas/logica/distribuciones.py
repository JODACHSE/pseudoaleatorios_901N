"""Cuantiles de la normal estándar y de la Chi-cuadrada, calculados con
aproximaciones numéricas puras en Python (sin scipy ni tablas externas),
para no añadir dependencias fuera del stack pedido (Flask + stdlib).

- `normal_ppf`: aproximación racional de Peter J. Acklam para la inversa
  de la CDF normal estándar (z tal que P(Z ≤ z) = p). Precisión ~1e-9.
- `chi2_ppf`: aproximación de Wilson-Hilferty para el cuantil de una
  Chi-cuadrada con `df` grados de libertad. Precisión adecuada para fines
  didácticos (error típico < 0.1 en los rangos usados en el curso).
- `ks_valor_critico`: valor crítico asintótico de Kolmogorov (fórmula de
  Kolmogorov-Smirnov de dos colas), razonable para n moderado/grande.
"""

from __future__ import annotations

import math


def normal_ppf(p: float) -> float:
    """Inversa de la CDF normal estándar (cuantil z_p)."""
    if not (0 < p < 1):
        raise ValueError("p debe estar estrictamente entre 0 y 1.")

    a = [-3.969683028665376e01, 2.209460984245205e02, -2.759285104469687e02,
         1.383577518672690e02, -3.066479806614716e01, 2.506628277459239e00]
    b = [-5.447609879822406e01, 1.615858368580409e02, -1.556989798598866e02,
         6.680131188771972e01, -1.328068155288572e01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e00,
         -2.549732539343734e00, 4.374664141464968e00, 2.938163982698783e00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00,
         3.754408661907416e00]

    p_bajo, p_alto = 0.02425, 1 - 0.02425

    if p < p_bajo:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    if p <= p_alto:
        q = p - 0.5
        r = q * q
        return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
               (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    q = math.sqrt(-2 * math.log(1 - p))
    return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)


def chi2_ppf(p: float, df: int) -> float:
    """Cuantil p de una Chi-cuadrada con `df` grados de libertad
    (aproximación de Wilson-Hilferty)."""
    if df <= 0:
        raise ValueError("Los grados de libertad deben ser un entero positivo.")
    z = normal_ppf(p)
    valor = df * (1 - 2 / (9 * df) + z * math.sqrt(2 / (9 * df))) ** 3
    return max(valor, 0.0)


def ks_valor_critico(alpha: float, n: int) -> float:
    """Valor crítico asintótico D(alpha, n) de la prueba Kolmogorov-Smirnov
    de dos colas: D_alpha ≈ sqrt(-0.5 · ln(alpha / 2)) / sqrt(n)."""
    return math.sqrt(-0.5 * math.log(alpha / 2)) / math.sqrt(n)
