import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, migrate
from app.api.expenses import bp as expenses_bp
from flasgger import Flasgger

load_dotenv()

def create_app(config_object='app.settings'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Initialize Flasgger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"
    }
    swagger = Flasgger(app, config=swagger_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(expenses_bp, url_prefix='/expenses')

    return app
