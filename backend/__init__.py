import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass

db:SQLAlchemy = SQLAlchemy(model_class=BaseModel)

@click.command("init-db")
@with_appcontext
def init_db_command():
    click.echo("Dropping existing tables...")
    db.drop_all()
    click.echo("Creating tables...")
    db.create_all()
    click.echo("✅ Initialized database.")

@click.command("init-db-data")
@click.argument('amount_multiplier', default=1)
@with_appcontext
def init_db_data_command(amount_multiplier: int = 1):
    from .database.dummy_data import init_db_data

    click.echo("Initializing database with fake data...")
    message = init_db_data(round(max(1, amount_multiplier)))
    click.echo(message)