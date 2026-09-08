"""Fábrica de la aplicación Flask.

Arquitectura del proyecto:

    app/
      inicio/          -> blueprint con la página de inicio (portada del curso)
      generadores/      -> blueprint con los métodos de generación de números
                           pseudoaleatorios (directos y congruenciales)
        logica/          -> funciones puras de cálculo (sin Flask), fáciles
                           de reutilizar y de probar por separado
      pruebas/           -> blueprint con las pruebas estadísticas
                           (medias, varianza, uniformidad, independencia)
        logica/          -> funciones puras de cálculo de cada prueba
      templates/         -> HTML (Jinja2), organizado por blueprint
      static/            -> CSS y JS compartidos (Bootstrap 5 + estilos propios)

Cada blueprint solo conoce Flask (rutas, formularios, `render_template`);
toda la matemática vive en los módulos `logica/`, que no dependen de Flask
y se pueden importar y probar de forma aislada.
"""

from flask import Flask

from .config import Config


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    from .inicio import bp as inicio_bp
    from .generadores import bp as generadores_bp
    from .pruebas import bp as pruebas_bp

    app.register_blueprint(inicio_bp)
    app.register_blueprint(generadores_bp, url_prefix="/generadores")
    app.register_blueprint(pruebas_bp, url_prefix="/pruebas")

    return app
