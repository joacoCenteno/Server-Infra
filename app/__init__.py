import logging
from flask import Flask, jsonify
from flask_cors import CORS
from app.config import Config
from app.models import db
from app.routes import api_bp

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def create_app(config_class=Config, config_override=None):
    app = Flask(__name__)
    app.config.from_object(config_class)
    if config_override:
        app.config.update(config_override)

    # Permitir CORS para permitir solicitudes desde cualquier origen
    CORS(app)

    # Inicializar Base de Datos
    db.init_app(app)

    # Registrar el Blueprint con todas las rutas
    app.register_blueprint(api_bp)

    # Intentar crear tablas si la base de datos está disponible
    with app.app_context():
        try:
            db.create_all()
            logger.info("Tablas de PostgreSQL verificadas/creadas exitosamente.")
        except Exception as e:
            logger.warning(
                "Aviso: No se pudo conectar a la base de datos PostgreSQL automáticamente al iniciar.\n"
                f"Detalle: {e}\n"
                "Asegúrate de que PostgreSQL esté corriendo y la base de datos configurada en .env exista."
            )

    # Manejadores de errores globales para respuestas JSON limpias
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'error': 'Recurso no encontrado',
            'detail': 'La URL solicitada no existe en esta API.'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Error interno del servidor',
            'detail': 'Ocurrió un problema inesperado en el servidor.'
        }), 500

    return app
