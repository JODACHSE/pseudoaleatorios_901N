"""Utilidades compartidas por las pruebas estadísticas."""

from __future__ import annotations


def parse_decimales(texto: str, minimo: int = 1, exigir_unitario: bool = True) -> list[float]:
    """Convierte una lista de números Ri separados por coma en flotantes.

    `exigir_unitario` valida que cada valor esté en [0, 1], como corresponde
    a un conjunto de números pseudoaleatorios Ri.
    """
    partes = [p.strip() for p in (texto or "").replace("\n", ",").split(",") if p.strip() != ""]
    if len(partes) < minimo:
        raise ValueError(f"Debes ingresar al menos {minimo} valores de Ri, separados por coma.")
    try:
        valores = [float(p) for p in partes]
    except ValueError:
        raise ValueError("Todos los valores deben ser números (usa punto decimal), separados por coma.")
    if exigir_unitario and any(v < 0 or v > 1 for v in valores):
        raise ValueError("Todos los valores de Ri deben estar en el intervalo [0, 1].")
    return valores


NIVELES_SIGNIFICANCIA = ["0.01", "0.05", "0.10"]


def parse_alpha(texto: str) -> float:
    texto = (texto or "0.05").strip()
    try:
        alpha = float(texto)
    except ValueError:
        raise ValueError("El nivel de significancia (α) debe ser un número, p. ej. 0.05.")
    if not (0 < alpha < 1):
        raise ValueError("El nivel de significancia (α) debe estar entre 0 y 1.")
    return alpha
