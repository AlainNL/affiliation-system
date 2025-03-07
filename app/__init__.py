from flask import Flask, jsonify
from app.api import register_blueprints
from app.utils.error_handlers import register_error_handlers

def create_app(config=None):

    app = Flask(__name__)

    @app.route('/')
    def home():
        return jsonify({
            "message": "Welcome to API Membership",
            "success": True
    })

    app.config.update({
        'DEBUG': True,
        'JSON_SORT_KEYS': False,
    })

    if config:
        app.config.update(config)

    register_blueprints(app)

    register_error_handlers(app)


    return app
