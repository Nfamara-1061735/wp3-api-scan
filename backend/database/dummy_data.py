# data_generation.py
import random

import click

from backend.database.models import Users, Organizations, UserOrganization, OrganizationType, LimitationsModel, \
    PeerExperts, PeerExpertsLimitations, ContactPreferences
from backend import db
from faker import Faker


# Very simple wrapper for message logging
def print_message(message):
    click.echo(message)

def generate_dummy_users(fake:Faker):
    print_message("Generating dummy user data...")
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

    return fake_users

def generate_organization_types():
    print_message("Importing organization types...")
    organization_type_data = [
        "commerciëel",
        "non-profit"
    ]
    organization_types = [OrganizationType(type=organization_type) for organization_type in organization_type_data]

    return organization_types

def generate_dummy_organizations(fake:Faker, organization_types:list[OrganizationType]):
    print_message("Generating dummy organization data...")

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
            organization_type_id=random.choice(organization_types).organization_type_id
            # Randomly assign to an existing organization type
        )
        fake_organizations.append(fake_organization)

    return fake_organizations


def generate_user_organization_relationships(fake_users, fake_organizations):
    print_message("Generating user-organization relationships...")
    user_organizations = []

    for user in fake_users:
        if random.random() < 0.5:  # 50% chance the user will have any organization
            organizations_count = 1 if random.random() < 0.9 else 2
            organizations_assigned = random.sample(fake_organizations, organizations_count)

            for organization in organizations_assigned:
                is_admin = random.choice([True, False])
                user_organization = UserOrganization(
                    user_id=user.user_id,
                    organization_id=organization.organization_id,
                    is_admin=is_admin
                )
                user_organizations.append(user_organization)

    return user_organizations


def generate_limitations():
    print_message("Importing limitations data...")
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

    limitations = [LimitationsModel(limitation=limitation) for limitation in limitations_data]

    return limitations


def generate_contact_preferences():
    print_message("Importing contact preferences...")
    organization_type_data = [
        "telefonisch",
        "email"
    ]
    organization_types = [ContactPreferences(type=organization_type) for organization_type in organization_type_data]

    return organization_types


def generate_peer_experts(fake: Faker, user_organizations: list[UserOrganization], fake_users: list[Users],
                          contact_preferences: list[ContactPreferences]):
    print_message("Generating dummy peer experts data...")
    peer_experts = []

    for user in fake_users:
        # Only assign to users not in any organization for now
        if not any(user_organization.user_id == user.user_id for user_organization in user_organizations):
            has_supervisor = random.choice([True, False])
            peer_expert = PeerExperts(
                postal_code=fake.postcode(),
                gender=random.choice(['man', 'vrouw']),
                birth_date=fake.date_of_birth(minimum_age=1, maximum_age=65),
                tools_used=fake.word(),
                short_bio=fake.text(max_nb_chars=300),
                special_notes=fake.text(max_nb_chars=200),
                accepted_terms=random.choice([True, False]),
                has_supervisor=has_supervisor,
                supervisor_or_guardian_name=fake.name() if has_supervisor else None,
                availability_notes=fake.text(max_nb_chars=100),
                contact_preference_id=random.choice(contact_preferences).contact_preference_id,
                user_id=user.user_id
            )
            peer_experts.append(peer_expert)

    return peer_experts


def generate_peer_experts_limitations(peer_experts: list[PeerExperts], limitations: list[LimitationsModel]):
    print_message("Assigning limitations to peer experts...")
    peer_experts_limitations = []

    for peer_expert in peer_experts:
        # Randomly assign 1 to 3 limitations to each peer expert
        assigned_limitations = random.sample(limitations, random.randint(1, 3))

        for limitation in assigned_limitations:
            peer_expert_limitation = PeerExpertsLimitations(
                limitation_id=limitation.limitation_id,
                peer_expert_id=peer_expert.peer_expert_id
            )
            peer_experts_limitations.append(peer_expert_limitation)

    return peer_experts_limitations

def init_db_data():
    # Drop all tables and create new ones
    print_message("Dropping existing tables...")
    db.drop_all()
    print_message("Creating tables...")
    db.create_all()
    print_message("✅ Initialized database.")

    fake = Faker(['nl_NL', 'nl_BE', 'fr_FR', 'en_GB'])

    # Generate fake data
    fake_users = generate_dummy_users(fake)
    db.session.bulk_save_objects(fake_users, return_defaults=True)

    organization_types = generate_organization_types()
    db.session.bulk_save_objects(organization_types, return_defaults=True)

    fake_organizations = generate_dummy_organizations(fake, organization_types)
    db.session.bulk_save_objects(fake_organizations, return_defaults=True)

    user_organizations = generate_user_organization_relationships(fake_users, fake_organizations)
    db.session.bulk_save_objects(user_organizations)

    limitations = generate_limitations()
    db.session.bulk_save_objects(limitations, return_defaults=True)

    contact_preferences = generate_contact_preferences()
    db.session.bulk_save_objects(contact_preferences, return_defaults=True)

    peer_experts = generate_peer_experts(fake, user_organizations, fake_users, contact_preferences)
    db.session.bulk_save_objects(peer_experts, return_defaults=True)

    peer_experts_limitations = generate_peer_experts_limitations(peer_experts, limitations)
    db.session.bulk_save_objects(peer_experts_limitations)

    db.session.commit()

    return "✅ Added dummy data to database"