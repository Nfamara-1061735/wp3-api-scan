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
    app = Flask(__name__)

    # Config flask application
    app.config['SECRET_KEY'] = "dev"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)
    app.cli.add_command(init_db_command)

    from backend.database import models

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
@with_appcontext
def init_db_command():
    click.echo("Dropping existing tables...")
    db.drop_all()
    click.echo("Creating tables...")
    db.create_all()

    from faker import Faker
    from backend.database.models import Users
    import random

    # Create an instance of the faker class with some randomly selected locales
    fake = Faker(['nl_NL', 'nl_BE', 'fr_FR', 'en_GB'])

    # Generate fake data
    click.echo("Generating fake user data...")

    # Create 10-25 fake users
    fake_users = []
    for _ in range(random.randrange(10, 25)):
        password = fake.password()  # generate fake password
        salt = fake.uuid4()  # generate fake salt

        fake_user = Users(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            password=password,
            salt=salt,
        )
        fake_users.append(fake_user)

    # Add fake data to the database
    click.echo("Adding fake data to the database...")
    db.session.bulk_save_objects(fake_users)
    db.session.commit()

    click.echo("✅ Initialized database and added fake data.")