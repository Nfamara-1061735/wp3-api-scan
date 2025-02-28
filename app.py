from flask import Flask
from frontend import frontend_bp
from backend import db, init_db_command, init_db_data_command


def create_app():
    """Create and configure an instance of the Flask application"""
    # Create flask instance
    app = Flask(__name__)

    # Config flask application
    app.config['SECRET_KEY'] = "dev"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_db_data_command)

    from backend.database import models

    # Register blueprints
    app.register_blueprint(frontend_bp)
    # app.register_blueprint(api_bp, url_prefix='/api')  # API routes with '/api' prefix

    return app


# Debug when running this script directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
