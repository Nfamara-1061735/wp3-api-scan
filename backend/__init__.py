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
    from .database.models import Users, Organizations, UserOrganization, OrganizationType, LimitationsModel
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
    click.echo("Adding fake user data to the database...")
    db.session.bulk_save_objects(fake_users, return_defaults=True)
    db.session.commit()

    # Generate fake organization data
    click.echo("Generating fake organization data...")

    organization_type_data = [
        "commerciëel",
        "non-profit"
    ]

    # Add each organization type to the database
    organization_types = [OrganizationType(type=organization_type) for organization_type in organization_type_data]
    db.session.bulk_save_objects(organization_types)
    db.session.commit()

    # Create the fake organizations
    fake_organizations = []
    for _ in range(random.randrange(5, 15)):  # Create 5-15 fake organizations
        fake_organization = Organizations(
            name=fake.company(),
            website=fake.url(),
            description=fake.text(max_nb_chars=200),
            contact_person=fake.name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            additional_information=fake.text(max_nb_chars=200),
            organization_type_id=random.randint(1, len(organization_type_data) + 1)  # Randomly assign to an existing organization type
        )
        fake_organizations.append(fake_organization)

    # Add fake organizations to the database
    click.echo("Adding fake organization data to the database...")
    db.session.bulk_save_objects(fake_organizations, return_defaults=True)
    db.session.commit()

    # Generate user-organization relationships (assigning mostly 1 organization, some to 2 organizations)
    click.echo("Generating user-organization relationships...")

    user_organizations = []
    for user in fake_users:
        if random.random() < 0.5:  # 50% chance the user will have any organization
            # Decide the amount of organization this user will be in
            organizations_count = 1 if random.random() < 0.9 else 2

            # Randomly assign the user to the selected amount of organizations
            organizations_assigned = random.sample(fake_organizations, organizations_count)

            for organization in organizations_assigned:
                # Randomly decide if the user is an admin or not
                is_admin = random.choice([True, False])
                user_organization = UserOrganization(
                    user_id=user.user_id,
                    organization_id=organization.organization_id,
                    is_admin=is_admin
                )
                user_organizations.append(user_organization)

    # Add user-organization relationships to the database
    click.echo("Adding user-organization relationships to the database...")
    db.session.bulk_save_objects(user_organizations)
    db.session.commit()

    # Limitations Data
    click.echo("Adding limitations data to the database...")

    limitations_data = [
        # Auditieve beperkingen
        "Doof",
        "Slechthorend",
        "Doofblind",

        # Visuele beperkingen
        "Blind",
        "Slechtziend",
        "Kleurenblind",
        "Doofblind",

        # Motorische / lichamelijke beperkingen
        "Amputatie en mismaaktheid",
        "Artritus",
        "Fibromyalgie",
        "Reuma",
        "Verminderde handvaardigheid",
        "Spierdystrofie",
        "RSI",
        "Tremor en Spasmen",
        "Quadriplegie of tetraplegie",

        # Cognitieve / neurologische beperkingen
        "ADHD",
        "Autisme",
        "Dyslexie",
        "Dyscalculie",
        "Leerstoornis",
        "Geheugen beperking",
        "Multiple Sclerose",
        "Epilepsie",
        "Migraine"
    ]

    # Add each limitation to the database
    limitations = [LimitationsModel(limitation=limitation) for limitation in limitations_data]
    db.session.bulk_save_objects(limitations)
    db.session.commit()

    click.echo("✅ Initialized database and added fake data.")