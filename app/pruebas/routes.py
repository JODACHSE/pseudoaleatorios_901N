from flask import render_template, request, flash

from . import bp
from .logica.comunes import parse_decimales, parse_alpha
from .logica.pruebas_estadisticas import (
    prueba_medias,
    prueba_varianza,
    prueba_chi_cuadrada,
    prueba_kolmogorov_smirnov,
    prueba_corridas,
)

# Conjunto de ejemplo (50 valores de Ri) tomado del ejemplo de la prueba de
# corridas del documento de clase, reutilizado como valor por defecto en
# las 5 pruebas para que cualquiera pueda ver un resultado con solo
# presionar el botón.
RI_EJEMPLO = (
    "0.809, 0.042, 0.432, 0.538, 0.225, 0.88, 0.688, 0.772, 0.036, 0.854, "
    "0.397, 0.266, 0.821, 0.897, 0.07, 0.721, 0.087, 0.35, 0.779, 0.482, "
    "0.136, 0.855, 0.453, 0.197, 0.444, 0.799, 0.089, 0.691, 0.545, 0.857, "
    "0.692, 0.055, 0.348, 0.373, 0.436, 0.29, 0.015, 0.834, 0.599, 0.724, "
    "0.564, 0.709, 0.946, 0.754, 0.677, 0.128, 0.012, 0.498, 0.6, 0.913"
)


@bp.route("/medias", methods=["GET", "POST"])
def medias():
    resultado = None
    ri = None
    valores = {"valores": RI_EJEMPLO, "alpha": "0.05"}

    if request.method == "POST":
        valores["valores"] = request.form.get("valores", "")
        valores["alpha"] = request.form.get("alpha", "0.05")
        try:
            ri = parse_decimales(valores["valores"], minimo=2)
            alpha = parse_alpha(valores["alpha"])
            resultado = prueba_medias(ri, alpha)
        except ValueError as err:
            flash(str(err), "danger")
            ri = None

    return render_template("pruebas/medias.html", resultado=resultado, ri=ri, valores=valores)


@bp.route("/varianza", methods=["GET", "POST"])
def varianza():
    resultado = None
    ri = None
    valores = {"valores": RI_EJEMPLO, "alpha": "0.05"}

    if request.method == "POST":
        valores["valores"] = request.form.get("valores", "")
        valores["alpha"] = request.form.get("alpha", "0.05")
        try:
            ri = parse_decimales(valores["valores"], minimo=2)
            alpha = parse_alpha(valores["alpha"])
            resultado = prueba_varianza(ri, alpha)
        except ValueError as err:
            flash(str(err), "danger")
            ri = None

    return render_template("pruebas/varianza.html", resultado=resultado, ri=ri, valores=valores)


@bp.route("/chi-cuadrada", methods=["GET", "POST"])
def chi_cuadrada():
    resultado = None
    ri = None
    valores = {"valores": RI_EJEMPLO, "alpha": "0.05", "intervalos": ""}

    if request.method == "POST":
        valores["valores"] = request.form.get("valores", "")
        valores["alpha"] = request.form.get("alpha", "0.05")
        valores["intervalos"] = request.form.get("intervalos", "")
        try:
            ri = parse_decimales(valores["valores"], minimo=5)
            alpha = parse_alpha(valores["alpha"])
            texto_m = valores["intervalos"].strip()
            m = None
            if texto_m:
                m = int(texto_m)
                if m < 2:
                    raise ValueError("La cantidad de sub-intervalos (m) debe ser al menos 2.")
            resultado = prueba_chi_cuadrada(ri, alpha, m)
        except ValueError as err:
            flash(str(err), "danger")
            ri = None

    return render_template("pruebas/chi_cuadrada.html", resultado=resultado, ri=ri, valores=valores)


@bp.route("/kolmogorov-smirnov", methods=["GET", "POST"])
def kolmogorov_smirnov():
    resultado = None
    ri = None
    valores = {"valores": RI_EJEMPLO, "alpha": "0.05"}

    if request.method == "POST":
        valores["valores"] = request.form.get("valores", "")
        valores["alpha"] = request.form.get("alpha", "0.05")
        try:
            ri = parse_decimales(valores["valores"], minimo=2)
            alpha = parse_alpha(valores["alpha"])
            resultado = prueba_kolmogorov_smirnov(ri, alpha)
        except ValueError as err:
            flash(str(err), "danger")
            ri = None

    return render_template("pruebas/kolmogorov_smirnov.html", resultado=resultado, ri=ri, valores=valores)


@bp.route("/corridas", methods=["GET", "POST"])
def corridas():
    resultado = None
    ri = None
    valores = {"valores": RI_EJEMPLO, "alpha": "0.05"}

    if request.method == "POST":
        valores["valores"] = request.form.get("valores", "")
        valores["alpha"] = request.form.get("alpha", "0.05")
        try:
            ri = parse_decimales(valores["valores"], minimo=10)
            alpha = parse_alpha(valores["alpha"])
            resultado = prueba_corridas(ri, alpha)
        except ValueError as err:
            flash(str(err), "danger")
            ri = None

    return render_template("pruebas/corridas.html", resultado=resultado, ri=ri, valores=valores)
