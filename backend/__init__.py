import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass

db:SQLAlchemy = SQLAlchemy(model_class=BaseModel)

def create_app():
    """Create and configure an instance of the Flask application"""
    # Create flask instance
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static',static_url_path='/')


    # Config flask application
    app.config['SECRET_KEY'] = "dev"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    app.cli.add_command(init_db_command)
    app.cli.add_command(init_db_data_command)

    from backend.database import models

    from backend.api import api
    api.init_app(app)

    return app

@click.command("init-db")
@with_appcontext
def init_db_command():
    click.echo("Dropping existing tables...")
    db.drop_all()
    click.echo("Creating tables...")
    db.create_all()
    click.echo("✅ Initialized database.")

@click.command("init-db-data")
@click.argument('amount_multiplier', default=100)
@with_appcontext
def init_db_data_command(amount_multiplier: int = 1):
    from .database.dummy_data import init_db_data

    click.echo("Initializing database with fake data...")
    message = init_db_data(round(max(1, amount_multiplier)))
    click.echo(message)