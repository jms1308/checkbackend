import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, migrate
from app.api.expenses import bp as expenses_bp

load_dotenv()

def create_app(config_object='app.settings'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(expenses_bp, url_prefix='/expenses')

    return app
