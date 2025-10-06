import os 
from datetime import timedelta

from flask import Flask
from flask_talisman import Talisman
from flask_seasurf import SeaSurf

from backend.api import api_bp
from frontend import frontend_bp
from backend import db, init_db_command, init_db_data_command


def create_app():
    """Create and configure an instance of the Flask application"""
    # Create flask instance
    app = Flask(__name__)

    # Config flask application
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI='sqlite:///database.db',

        #cookies en sessies
        SESSION_COOKIE_SAMESITE='Lax',  
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=False, #op true zetten als we de app echt zouden launchen dan zou het Https zijn ipv http     
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=60),
    )


    db.init_app(app)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_db_data_command)

    #security headers (CSP)
    csp = { 
        'default-src': ["'self'"],
        'script-src':  ["'self'"],
        'style-src':   ["'self'", "'unsafe-inline'"]
    }
    
    Talisman(
        app,
        content_security_policy=csp,
        frame_options='SAMEORIGIN',      
        referrer_policy='no-referrer',
        force_https=False
    )



    from backend.database import models

    # Register blueprints
    app.register_blueprint(frontend_bp)
    app.register_blueprint(api_bp, url_prefix='/api')  # API routes with '/api' prefix

    print("🔍 Geregistreerde routes:") # Debugging
    for rule in app.url_map.iter_rules():
        print(rule)

    return app


# Debug when running this script directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
