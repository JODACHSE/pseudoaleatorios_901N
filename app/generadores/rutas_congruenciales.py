from flask import render_template, request, flash, session

from . import bp
from .logica.comunes import parse_semillas
from .logica.metodos_congruenciales import (
    generar_congruencial_lineal,
    generar_congruencial_multiplicativo,
    generar_congruencial_aditivo,
    evaluar_hull_dobell,
    generar_secuencia_con_periodo,
)
from .logica.validacion import validar_secuencia
from .logica.comparacion import resumen_ligero, comparar


@bp.route("/congruencial-lineal", methods=["GET", "POST"])
def congruencial_lineal():
    resultados = None
    validacion = None
    valores = {"x0": "37", "a": "21", "c": "1", "m": "65536", "cantidad": "200"}

    if request.method == "POST":
        for campo in ("x0", "a", "c", "m", "cantidad"):
            valores[campo] = request.form.get(campo, "")
        try:
            x0 = int(valores["x0"])
            a = int(valores["a"])
            c = int(valores["c"])
            m = int(valores["m"])
            cantidad = int(valores["cantidad"])
            if m <= 0:
                raise ValueError("El módulo (m) debe ser un entero positivo.")
            if x0 < 0 or a < 0 or c < 0:
                raise ValueError("X0, a y c deben ser enteros no negativos.")
            if not (1 <= cantidad <= 2000):
                raise ValueError("La cantidad de números debe estar entre 1 y 2000.")
            resultados = generar_congruencial_lineal(x0, a, c, m, cantidad)
            validacion = validar_secuencia([fila["ri"] for fila in resultados])
            if validacion:
                session["comparacion_congruencial_lineal"] = resumen_ligero(
                    validacion,
                    {"x0": x0, "a": a, "c": c, "m": m, "cantidad": cantidad},
                    "Congruencial lineal",
                )
        except ValueError as err:
            flash(str(err) if str(err) else "Revisa los datos ingresados: deben ser números enteros válidos.", "danger")

    return render_template(
        "generadores/congruencial_lineal.html",
        resultados=resultados,
        validacion=validacion,
        valores=valores,
    )


@bp.route("/congruencial-multiplicativo", methods=["GET", "POST"])
def congruencial_multiplicativo():
    resultados = None
    valores = {"x0": "17", "a": "21", "m": "32", "cantidad": "8"}

    if request.method == "POST":
        for campo in ("x0", "a", "m", "cantidad"):
            valores[campo] = request.form.get(campo, "")
        try:
            x0 = int(valores["x0"])
            a = int(valores["a"])
            m = int(valores["m"])
            cantidad = int(valores["cantidad"])
            if m <= 0:
                raise ValueError("El módulo (m) debe ser un entero positivo.")
            if x0 <= 0:
                raise ValueError("La semilla X0 debe ser un entero positivo (si es 0, la secuencia se queda en 0).")
            if a <= 0:
                raise ValueError("El multiplicador (a) debe ser un entero positivo.")
            if not (1 <= cantidad <= 500):
                raise ValueError("La cantidad de números debe estar entre 1 y 500.")
            resultados = generar_congruencial_multiplicativo(x0, a, m, cantidad)
        except ValueError as err:
            flash(str(err) if str(err) else "Revisa los datos ingresados: deben ser números enteros válidos.", "danger")

    return render_template(
        "generadores/congruencial_multiplicativo.html",
        resultados=resultados,
        valores=valores,
    )


@bp.route("/congruencial-aditivo", methods=["GET", "POST"])
def congruencial_aditivo():
    resultados = None
    orden = None
    valores = {"semillas": "65, 89, 98, 3, 69", "m": "100", "cantidad": "7"}

    if request.method == "POST":
        valores["semillas"] = request.form.get("semillas", "")
        valores["m"] = request.form.get("m", "")
        valores["cantidad"] = request.form.get("cantidad", "")
        try:
            semillas = parse_semillas(valores["semillas"], minimo=2)
            if any(s < 0 for s in semillas):
                raise ValueError("Las semillas deben ser enteros no negativos.")
            m = int(valores["m"])
            cantidad = int(valores["cantidad"])
            if m <= 0:
                raise ValueError("El módulo (m) debe ser un entero positivo.")
            if not (1 <= cantidad <= 500):
                raise ValueError("La cantidad de números debe estar entre 1 y 500.")
            resultados = generar_congruencial_aditivo(semillas, m, cantidad)
            orden = len(semillas)
        except ValueError as err:
            flash(str(err) if str(err) else "Revisa los datos ingresados: deben ser números enteros válidos.", "danger")

    return render_template(
        "generadores/congruencial_aditivo.html",
        resultados=resultados,
        orden=orden,
        valores=valores,
    )


@bp.route("/periodo-maximo-congruencial-lineal", methods=["GET", "POST"])
def periodo_maximo_congruencial_lineal():
    analisis = None
    corridas = None
    valores = {"semillas": "6", "a": "13", "c": "7", "m": "8"}

    if request.method == "POST":
        valores["semillas"] = request.form.get("semillas", "")
        for campo in ("a", "c", "m"):
            valores[campo] = request.form.get(campo, "")
        try:
            semillas = parse_semillas(valores["semillas"], minimo=1)
            a = int(valores["a"])
            c = int(valores["c"])
            m = int(valores["m"])
            if m <= 0:
                raise ValueError("El módulo (m) debe ser un entero positivo.")
            if a < 0 or c < 0:
                raise ValueError("a y c deben ser enteros no negativos.")
            if any(s < 0 for s in semillas):
                raise ValueError("Las semillas (X0) deben ser enteros no negativos.")

            analisis = evaluar_hull_dobell(a, c, m)
            limite = min(m, 2000)
            corridas = []
            for x0 in semillas:
                resultados, periodo, inicio_ciclo = generar_secuencia_con_periodo(x0, a, c, m, limite)
                corridas.append({
                    "x0": x0,
                    "resultados": resultados,
                    "periodo": periodo,
                    "inicio_ciclo": inicio_ciclo,
                })
        except ValueError as err:
            flash(str(err) if str(err) else "Revisa los datos ingresados: deben ser números enteros válidos.", "danger")

    return render_template(
        "generadores/periodo_maximo.html",
        analisis=analisis,
        corridas=corridas,
        valores=valores,
    )


@bp.route("/comparacion")
def comparacion():
    """Actividad adicional (punto 6): compara el comportamiento estadístico
    de los 2 algoritmos elegidos (congruencial lineal y productos medios)
    usando el último resumen de validación que cada página guardó en
    sesión al generar una secuencia con n >= 30."""
    comp_lineal = session.get("comparacion_congruencial_lineal")
    comp_productos = session.get("comparacion_productos_medios")

    return render_template(
        "generadores/comparacion.html",
        comp_lineal=comp_lineal,
        comp_productos=comp_productos,
        resumen=comparar(comp_lineal, comp_productos),
    )
