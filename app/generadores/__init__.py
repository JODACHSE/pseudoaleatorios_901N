from flask import Blueprint

bp = Blueprint("generadores", __name__)

# Cada módulo registra sus rutas sobre `bp` al importarse.
from . import rutas_directos, rutas_congruenciales  # noqa: E402,F401
