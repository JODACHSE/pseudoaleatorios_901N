import os


class Config:
    """Configuración base. En un proyecto real, SECRET_KEY vendría de una
    variable de entorno; aquí se deja un valor por defecto solo para que
    `flash()` funcione de inmediato en desarrollo."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-de-desarrollo-901n-modelacion")
    JSON_SORT_KEYS = False
