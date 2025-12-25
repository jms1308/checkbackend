import os
from flask import Flask
from app.extensions import db, jwt, migrate
from app.auth import bp as auth_bp
from app.api.professions import bp as professions_bp
from app.api.employees import bp as employees_bp
from app.api.students import bp as students_bp
from app.api.test_results import bp as test_results_bp
from app.api.expenses import bp as expenses_bp

def create_app(config_object='app.settings'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(professions_bp, url_prefix='/professions')
    app.register_blueprint(employees_bp, url_prefix='/employees')
    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(test_results_bp, url_prefix='/test_results')
    app.register_blueprint(expenses_bp, url_prefix='/expenses')

    return app
