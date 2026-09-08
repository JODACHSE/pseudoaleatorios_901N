from flask import Blueprint

bp = Blueprint("pruebas", __name__)

from . import routes  # noqa: E402,F401
