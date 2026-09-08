from flask import render_template, request, flash

from . import bp
from .logica.comunes import parse_semillas
from .logica.metodos_directos import (
    generar_cuadrados_medios,
    generar_productos_medios,
    generar_multiplicador_constante,
)
from .logica.validacion import validar_secuencia


def _leer_digitos(valores: dict) -> int | None:
    """Lee el campo D del formulario. Vacío => se calcula automáticamente
    a partir de la cantidad de dígitos de la(s) semilla(s)."""
    texto = valores.get("digitos", "").strip()
    if texto == "":
        return None
    digitos = int(texto)
    if digitos <= 0:
        raise ValueError("La cantidad de dígitos (D) debe ser un entero positivo.")
    return digitos


@bp.route("/cuadrados-medios", methods=["GET", "POST"])
def cuadrados_medios():
    resultados = None
    digitos = None
    ciclo = None
    valores = {"semilla": "5735", "digitos": "", "cantidad": "10"}

    if request.method == "POST":
        valores["semilla"] = request.form.get("semilla", "")
        valores["digitos"] = request.form.get("digitos", "")
        valores["cantidad"] = request.form.get("cantidad", "")
        try:
            semilla = int(valores["semilla"])
            digitos_d = _leer_digitos(valores)
            cantidad = int(valores["cantidad"])
            if semilla <= 0:
                raise ValueError("La semilla debe ser un entero positivo.")
            if not (1 <= cantidad <= 500):
                raise ValueError("La cantidad de números debe estar entre 1 y 500.")
            resultados, digitos, ciclo = generar_cuadrados_medios(semilla, cantidad, digitos_d)
        except ValueError as err:
            flash(str(err) if str(err) else "Revisa los datos ingresados: deben ser números enteros válidos.", "danger")

    return render_template(
        "generadores/cuadrados_medios.html",
        resultados=resultados,
        digitos=digitos,
        ciclo=ciclo,
        valores=valores,
    )


@bp.route("/productos-medios", methods=["GET", "POST"])
def productos_medios():
    resultados = None
    digitos = None
    orden = None
    validacion = None
    valores = {"semillas": "5015, 5734", "digitos": "", "cantidad": "200"}

    if request.method == "POST":
        valores["semillas"] = request.form.get("semillas", "")
        valores["digitos"] = request.form.get("digitos", "")
        valores["cantidad"] = request.form.get("cantidad", "")
        try:
            semillas = parse_semillas(valores["semillas"], minimo=2)
            if any(s <= 0 for s in semillas):
                raise ValueError("Todas las semillas deben ser enteros positivos.")
            digitos_d = _leer_digitos(valores)
            cantidad = int(valores["cantidad"])
            if not (1 <= cantidad <= 2000):
                raise ValueError("La cantidad de números debe estar entre 1 y 2000.")
            resultados, digitos = generar_productos_medios(semillas, cantidad, digitos_d)
            orden = len(semillas)
            # Algoritmo seleccionado para la actividad adicional: valida
            # automáticamente la secuencia recién generada con las 4
            # pruebas (medias, varianza, Chi-cuadrada, corridas).
            validacion = validar_secuencia([fila["ri"] for fila in resultados])
        except ValueError as err:
            flash(str(err) if str(err) else "Revisa los datos ingresados: deben ser números enteros válidos.", "danger")

    return render_template(
        "generadores/productos_medios.html",
        resultados=resultados,
        digitos=digitos,
        orden=orden,
        validacion=validacion,
        valores=valores,
    )


@bp.route("/multiplicador-constante", methods=["GET", "POST"])
def multiplicador_constante():
    resultados = None
    digitos = None
    valores = {"semilla": "9803", "constante": "6965", "digitos": "", "cantidad": "10"}

    if request.method == "POST":
        valores["semilla"] = request.form.get("semilla", "")
        valores["constante"] = request.form.get("constante", "")
        valores["digitos"] = request.form.get("digitos", "")
        valores["cantidad"] = request.form.get("cantidad", "")
        try:
            semilla = int(valores["semilla"])
            constante = int(valores["constante"])
            digitos_d = _leer_digitos(valores)
            cantidad = int(valores["cantidad"])
            if semilla <= 0 or constante <= 0:
                raise ValueError("La semilla y la constante deben ser enteros positivos.")
            if not (1 <= cantidad <= 500):
                raise ValueError("La cantidad de números debe estar entre 1 y 500.")
            resultados, digitos = generar_multiplicador_constante(semilla, constante, cantidad, digitos_d)
        except ValueError as err:
            flash(str(err) if str(err) else "Revisa los datos ingresados: deben ser números enteros válidos.", "danger")

    return render_template(
        "generadores/multiplicador_constante.html",
        resultados=resultados,
        digitos=digitos,
        valores=valores,
    )
