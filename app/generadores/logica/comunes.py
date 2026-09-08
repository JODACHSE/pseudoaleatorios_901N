"""Utilidades compartidas por los distintos métodos de generación.

Este módulo no importa Flask: son funciones puras (mismos argumentos ->
mismo resultado), lo que las hace fáciles de reutilizar y de probar.
"""

from __future__ import annotations


def extraer_medio(numero: int, digitos: int) -> str:
    """Devuelve los `digitos` dígitos centrales de `numero`.

    Se centra sobre el ancho NATURAL del número (no se fuerza a 2×D):
    esto es justo lo que hace el ejemplo del documento de clase, donde
    Y3 = 101761 (6 dígitos) entrega X4 = 0176 tomando el centro de esos
    6 dígitos, no de 8. Solo se rellena con ceros a la izquierda en el
    caso borde en que `numero` tenga MENOS dígitos que `digitos`
    ("si no es posible obtener los D dígitos centrales, se completan
    con ceros a la izquierda").
    """
    texto = str(numero)
    if len(texto) < digitos:
        texto = texto.zfill(digitos)
    inicio = (len(texto) - digitos) // 2
    return texto[inicio: inicio + digitos]


def parse_semillas(texto: str, minimo: int = 1) -> list[int]:
    """Convierte una lista de semillas separadas por coma (p. ej. "5735, 6283")
    en enteros. `minimo` es la cantidad mínima de semillas exigida."""
    partes = [p.strip() for p in (texto or "").split(",") if p.strip() != ""]
    if len(partes) < minimo:
        raise ValueError(
            f"Debes ingresar al menos {minimo} semilla(s), separadas por coma."
        )
    try:
        return [int(p) for p in partes]
    except ValueError:
        raise ValueError("Todas las semillas deben ser números enteros, separados por coma.")


def factores_primos(n: int) -> list[int]:
    """Factores primos distintos de `n` (usado en el análisis de período máximo)."""
    n = abs(n)
    factores = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factores.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factores.append(n)
    return factores
