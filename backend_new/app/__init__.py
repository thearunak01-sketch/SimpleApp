from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge

from app.config import Config
from app.extensions import db, jwt, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    if isinstance(config_class, dict):
        app.config.from_mapping(config_class)
    else:
        app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(
        app,
        origins=[app.config["FRONTEND_ORIGIN"]],
        supports_credentials=True,
        allow_headers=["Content-Type", "X-CSRF-TOKEN"],
        methods=["GET", "POST", "DELETE", "OPTIONS"],
    )

    from app.models.document import Document
    from app.models.image import Image
    from app.models.user import User
    from app.routes.auth import auth_bp
    from app.routes.documents import documents_bp
    from app.routes.images import images_bp
    from app.routes.profile import profile_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(profile_bp, url_prefix="/api")
    app.register_blueprint(images_bp, url_prefix="/api/images")
    app.register_blueprint(documents_bp, url_prefix="/api/documents")

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(_error):
        return jsonify({"error": "The upload is too large."}), 413

    @app.errorhandler(404)
    def handle_not_found(_error):
        return jsonify({"error": "Resource not found."}), 404

    @jwt.unauthorized_loader
    def handle_missing_token(_reason):
        return jsonify({"error": "Authentication is required."}), 401

    @jwt.invalid_token_loader
    def handle_invalid_token(_reason):
        return jsonify({"error": "Authentication token is invalid."}), 401

    @jwt.expired_token_loader
    def handle_expired_token(_jwt_header, _jwt_payload):
        return jsonify({"error": "Your session has expired."}), 401

    return app
