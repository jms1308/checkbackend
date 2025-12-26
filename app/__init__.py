import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, migrate
from app.api.expenses import bp as expenses_bp
from app.api.firestore import firestore_bp
from app.api.firestore_expenses import firestore_expenses_bp

load_dotenv()

def create_app(config_object='app.settings'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(expenses_bp, url_prefix='/expenses')
    app.register_blueprint(firestore_bp, url_prefix='/firestore')
    app.register_blueprint(firestore_expenses_bp, url_prefix='/firestore-expenses')

    return app
