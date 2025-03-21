import json
import random
from datetime import datetime, timedelta

import click

from backend.database.models import Users, Organizations, UserOrganization, OrganizationType, LimitationsModel, \
    PeerExperts, PeerExpertsLimitations, ContactPreferences, ResearchStatus, ResearchTypesModel, Research, \
    PeerExpertsResearchTypes, ResearchLimitations, UsersStichtingAccessibility, PeerExpertStatus, RegistrationStatus, \
    PeerExpertRegistration
from backend import db
from faker import Faker
from backend.database.models.api_keys_model import ApiKeys
import secrets

from backend.utils.password import hash_password, generate_salt


def generate_api_keys():
    print_message("API-keys worden gegenereerd en toegevoegd...")

    api_keys_data = [
        ("organisatie_1", secrets.token_hex(8)),
        ("organisatie_2", secrets.token_hex(8))
    ]

    existing_keys = {key.api_key for key in ApiKeys.query.all()}

    new_api_keys = [
        ApiKeys(api_key=key, organization_name=org_name)
        for org_name, key in api_keys_data if key not in existing_keys
    ]

    if new_api_keys:
        db.session.add_all(new_api_keys)
        db.session.commit()
        print_message(f"{len(new_api_keys)} nieuwe API-key toegevoegd.")
    else:
        print_message("Geen nieuwe API-key toegevoegd, deze key bestaat al.")

    return new_api_keys

# Very simple wrapper for message logging
def print_message(message):
    click.echo(message)

def generate_dummy_users(fake: Faker, multiplier=1):
    print_message("Generating dummy user data...")
    fake_users = []
    for i in range(random.randrange(10 * multiplier, 25 * multiplier)):
        email = fake.unique.email()
        password = fake.binary(32)  # generate fake password
        salt = fake.binary(16)  # generate fake salt

        fake_user = Users(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=email,
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


def generate_dummy_organizations(fake: Faker, organization_types: list[OrganizationType], multiplier=1):
    print_message("Generating dummy organization data...")

    fake_organizations = []
    for _ in range(random.randrange(5 * multiplier, 15 * multiplier)):  # Create 5-15 fake organizations
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


def generate_user_organization_relationships(fake_users: list[Users], fake_organizations: list[Organizations],
                                             default_users: list[Users] = None):
    if default_users is None:
        default_users: list[Users] = []

    print_message("Generating user-organization relationships...")
    user_organizations = []

    for user in [*fake_users, *default_users]:
        if user in default_users or random.random() < 0.5:  # 50% chance the user will have any organization
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

    auditieve_beperkingen = [
        "Doof",
        "Slechthorend",
        "Doofblind"
    ]

    visuele_beperkingen = [
        "Blind",
        "Slechtziend",
        "Kleurenblind",
        "Doofblind"
    ]

    motorische_lichamelijke_beperkingen = [
        "Amputatie en mismaaktheid",
        "Artritus",
        "Fibromyalgie",
        "Reuma",
        "Verminderde handvaardigheid",
        "Spierdystrofie",
        "RSI",
        "Tremor en Spasmen",
        "Quadriplegie of tetraplegie"
    ]

    cognitieve_neurologische_beperkingen = [
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

    # Create the LimitationsModel instances
    limitations = []

    # Auditieve beperkingen
    limitations.extend(
        [LimitationsModel(limitation=limitation, limitation_category="Auditieve beperkingen") for limitation in
         auditieve_beperkingen])

    # Visuele beperkingen
    limitations.extend(
        [LimitationsModel(limitation=limitation, limitation_category="Visuele beperkingen") for limitation in
         visuele_beperkingen])

    # Motorische / lichamelijke beperkingen
    limitations.extend(
        [LimitationsModel(limitation=limitation, limitation_category="Motorische / lichamelijke beperkingen") for
         limitation in motorische_lichamelijke_beperkingen])

    # Cognitieve / neurologische beperkingen
    limitations.extend(
        [LimitationsModel(limitation=limitation, limitation_category="Cognitieve / neurologische beperkingen") for
         limitation in cognitieve_neurologische_beperkingen])

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
                          contact_preferences: list[ContactPreferences], peer_expert_statuses: list[PeerExpertStatus],
                          default_users: list[Users]):
    print_message("Generating dummy peer experts data...")
    peer_experts = []

    for user in [*fake_users, *default_users]:
        # Only assign to users not in any organization for now
        if user in default_users or (
        not any(user_organization.user_id == user.user_id for user_organization in user_organizations)):
            date_of_birth = fake.date_of_birth(minimum_age=1, maximum_age=65)

            # Enable supervisor if expert is under 18 years old, else randomly enable supervisor
            has_supervisor = True if (datetime.now().date() - date_of_birth).days / 365.242199 < 18 else random.choice(
                [True, False, False])

            peer_expert = PeerExperts(
                postal_code=fake.postcode(),
                gender=random.choice(['man', 'vrouw']),
                birth_date=date_of_birth,
                tools_used=fake.word(),
                short_bio=fake.text(max_nb_chars=300),
                special_notes=fake.text(max_nb_chars=200),
                accepted_terms=random.choice([True, False]),
                has_supervisor=has_supervisor,
                supervisor_or_guardian_name=fake.name() if has_supervisor else None,
                supervisor_or_guardian_email=fake.email() if has_supervisor else None,
                supervisor_or_guardian_phone=fake.phone_number() if has_supervisor else None,
                availability_notes=fake.text(max_nb_chars=100),
                contact_preference_id=random.choice(contact_preferences).contact_preference_id,
                peer_expert_status_id=random.choice(peer_expert_statuses).peer_expert_status_id,
                user_id=user.user_id
            )
            peer_experts.append(peer_expert)

    return peer_experts


def generate_peer_experts_limitations(peer_experts: list[PeerExperts], limitations: list[LimitationsModel]):
    print_message("Assigning limitations to peer experts...")
    peer_experts_limitations = []

    for peer_expert in peer_experts:
        # Randomly assign 1 to 3 limitations to each peer expert
        assigned_limitations = random.sample(limitations, random.randint(1, 5))

        for limitation in assigned_limitations:
            peer_expert_limitation = PeerExpertsLimitations(
                limitation_id=limitation.limitation_id,
                peer_expert_id=peer_expert.peer_expert_id
            )
            peer_experts_limitations.append(peer_expert_limitation)

    return peer_experts_limitations


def generate_research_statuses():
    print_message("Importing research statuses...")

    research_status_data = [
        "nieuw",
        "goedgekeurd",
        "afgekeurd",
        "gesloten"
    ]
    research_statuses = [ResearchStatus(status=research_status) for research_status in research_status_data]

    return research_statuses


def generate_peer_expert_statuses():
    print_message("Importing peer expert statuses...")

    research_status_data = [
        "nieuw",
        "goedgekeurd",
        "afgekeurd",
        "gesloten"
    ]
    research_statuses = [PeerExpertStatus(status=research_status) for research_status in research_status_data]

    return research_statuses


def generate_registration_statuses():
    print_message("Importing registration statuses...")

    research_status_data = [
        "nieuw",
        "goedgekeurd",
        "afgekeurd",
        "gesloten"
    ]
    research_statuses = [RegistrationStatus(status=research_status) for research_status in research_status_data]

    return research_statuses

def generate_research_types():
    print_message("Importing research types...")

    research_type_data = [
        "locatie",
        "telefonisch",
        "online"
    ]
    research_types = [ResearchTypesModel(type=research_type) for research_type in research_type_data]

    return research_types


def generate_researches(fake: Faker, research_statuses: list[ResearchStatus], research_types: list[ResearchTypesModel],
                        multiplier=1):
    print_message("Generating dummy organization data...")

    fake_researches = []
    for _ in range(random.randrange(5 * multiplier, 15 * multiplier)):
        # Start date
        start_date = fake.date_time_between_dates(datetime_start=datetime(2020, 1, 1),
                                                  datetime_end=datetime(2030, 1, 1))

        # End date
        random_days = random.randint(1, 24)
        random_hours = random.randint(0, 365)
        delta = timedelta(days=random_days, hours=random_hours)
        end_date = start_date + delta

        # Reward
        has_reward = random.choice([True, False])

        # Age
        target_min_age = random.randint(4, 65)
        target_max_age = random.randint(target_min_age, 65)

        fake_research = Research(
            title=fake.text(max_nb_chars=45),
            is_available=random.choice([True, False]),
            description=fake.text(max_nb_chars=500),
            start_date=start_date,
            end_date=end_date,
            location=fake.address(),
            has_reward=has_reward,
            reward=fake.text(max_nb_chars=45) if has_reward else None,
            target_min_age=target_min_age,
            target_max_age=target_max_age,
            status_id=random.choice(research_statuses).research_status_id,
            research_type_id=random.choice(research_types).research_type_id,
            limitations=[]
        )

        fake_researches.append(fake_research)

    return fake_researches


def get_researches(limitations_lookup):
    print_message("Generating dummy organization data...")

    researches_data = [
        {
            "title": "Albert Heijn",
            "is_available": True,
            "description": "Dit is een random omschrijving voor dit nieuwe onderzoek voor de Albert Heijn",
            "start_date": "01-01-2025",
            "end_date": "02-02-2025",
            "location": "Rotterdam",
            "has_reward": True,
            "reward": "Jaar lang korting",
            "target_min_age": 18,
            "target_max_age": 65,
            "status_id": 1,
            "research_type_id": 1,
            "limitation_ids": [1, 2]
        },
        {
            "title": "Jumbo",
            "is_available": True,
            "description": "Dit is een random omschrijving voor dit nieuwe onderzoek voor de Jumbo",
            "start_date": "01-03-2025",
            "end_date": "02-04-2025",
            "location": "Amsterdam",
            "has_reward": False,
            "reward": "50 euro voucher",
            "target_min_age": 20,
            "target_max_age": 70,
            "status_id": 1,
            "research_type_id": 2,
            "limitation_ids": [3, 4]
        },
        {
            "title": "Bol.com",
            "is_available": True,
            "description": "Dit is een random omschrijving voor dit nieuwe onderzoek voor bol.com",
            "start_date": "01-06-2025",
            "end_date": "31-12-2025",
            "location": "Nederland",
            "has_reward": True,
            "reward": "Een jaar lang geen bezorgkosten",
            "target_min_age": 16,
            "target_max_age": 80,
            "status_id": 1,
            "research_type_id": 3,
            "limitation_ids": []
        },
        {
            "title": "Dirk van den Broek",
            "is_available": True,
            "description": "Dit is een random omschrijving voor dit nieuwe onderzoek voor de Dirk",
            "start_date": "01-01-2025",
            "end_date": "02-02-2025",
            "location": "Rotterdam",
            "has_reward": True,
            "reward": "Jaar lang korting",
            "target_min_age": 18,
            "target_max_age": 65,
            "status_id": 2,
            "research_type_id": 1,
            "limitation_ids": [1, 2]
        },
        {
            "title": "Plus",
            "is_available": True,
            "description": "Dit is een random omschrijving voor dit nieuwe onderzoek voor de Plus",
            "start_date": "01-03-2025",
            "end_date": "02-04-2025",
            "location": "Amsterdam",
            "has_reward": False,
            "reward": "50 euro voucher",
            "target_min_age": 20,
            "target_max_age": 70,
            "status_id": 2,
            "research_type_id": 2,
            "limitation_ids": [3, 4]
        },
        {
            "title": "Gemeente Rotterdam",
            "is_available": True,
            "description": "Dit is een random omschrijving voor dit nieuwe onderzoek voor Gemeente Rotterdam",
            "start_date": "01-06-2025",
            "end_date": "31-12-2025",
            "location": "Nederland",
            "has_reward": True,
            "reward": "Een jaar lang geen bezorgkosten",
            "target_min_age": 16,
            "target_max_age": 80,
            "status_id": 2,
            "research_type_id": 3,
            "limitation_ids": []
        },
        {
            "title": "Hema",
            "is_available": True,
            "description": "Dit is een random omschrijving voor dit nieuwe onderzoek voor de Hema",
            "start_date": "01-01-2025",
            "end_date": "02-02-2025",
            "location": "Rotterdam",
            "has_reward": True,
            "reward": "Jaar lang korting",
            "target_min_age": 18,
            "target_max_age": 65,
            "status_id": 3,
            "research_type_id": 1,
            "limitation_ids": [1, 2]
        },
        {
            "title": "Primark",
            "is_available": True,
            "description": "Dit is een random omschrijving voor dit nieuwe onderzoek voor de primark",
            "start_date": "01-03-2025",
            "end_date": "02-04-2025",
            "location": "Amsterdam",
            "has_reward": False,
            "reward": "50 euro voucher",
            "target_min_age": 20,
            "target_max_age": 70,
            "status_id": 3,
            "research_type_id": 2,
            "limitation_ids": [3, 4]
        },
        {
            "title": "Marktplaats",
            "is_available": True,
            "description": "Dit is een random omschrijving voor dit nieuwe onderzoek voor Marktplaats",
            "start_date": "01-06-2025",
            "end_date": "31-12-2025",
            "location": "Nederland",
            "has_reward": True,
            "reward": "Een jaar lang geen bezorgkosten",
            "target_min_age": 16,
            "target_max_age": 80,
            "status_id": 3,
            "research_type_id": 3,
            "limitation_ids": []
        },
        {
            "title": "Bol.com2",
            "is_available": True,
            "description": "Dit is een random omschrijving voor dit nieuwe onderzoek voor de Bol.com2",
            "start_date": "01-01-2025",
            "end_date": "02-02-2025",
            "location": "Rotterdam",
            "has_reward": True,
            "reward": "Jaar lang korting",
            "target_min_age": 18,
            "target_max_age": 65,
            "status_id": 4,
            "research_type_id": 1,
            "limitation_ids": [1, 2]
        },
        {
            "title": "Albert Heijn2",
            "is_available": True,
            "description": "Dit is een random omschrijving voor dit nieuwe onderzoek voor de Albert Heijn2",
            "start_date": "01-03-2025",
            "end_date": "02-04-2025",
            "location": "Amsterdam",
            "has_reward": False,
            "reward": "50 euro voucher",
            "target_min_age": 20,
            "target_max_age": 70,
            "status_id": 4,
            "research_type_id": 2,
            "limitation_ids": [3, 4]
        },
        {
            "title": "Jumbo2",
            "is_available": True,
            "description": "Dit is een random omschrijving voor dit nieuwe onderzoek voor Jumbo2",
            "start_date": "01-06-2025",
            "end_date": "31-12-2025",
            "location": "Nederland",
            "has_reward": True,
            "reward": "Een jaar lang geen bezorgkosten",
            "target_min_age": 16,
            "target_max_age": 80,
            "status_id": 4,
            "research_type_id": 3,
            "limitation_ids": []
        }
    ]

    researches = []

    for data in researches_data:
        start_date = datetime.strptime(data["start_date"], "%d-%m-%Y").date()
        end_date = datetime.strptime(data["end_date"], "%d-%m-%Y").date()

        fake_research = Research(
            title=data["title"],
            is_available=data["is_available"],
            description=data["description"],
            start_date=start_date,
            end_date=end_date,
            location=data["location"],
            has_reward=data["has_reward"],
            reward=data["reward"],
            target_min_age=data["target_min_age"],
            target_max_age=data["target_max_age"],
            status_id=data["status_id"],
            research_type_id=data["research_type_id"],
        )

        if data["limitation_ids"]:
            matched_limitations = [limitations_lookup[lid] for lid in data["limitation_ids"]]
            fake_research.limitations.extend(matched_limitations)

        researches.append(fake_research)

    return researches


def generate_research_limitations(researches: list[Research], limitations: list[LimitationsModel]):
    print_message("Assigning limitations to peer researches...")
    research_limitations = []

    for research in researches:
        # Randomly assign 1 to 3 limitations to each research
        assigned_limitations = random.sample(limitations, random.randint(1, 3))

        for limitation in assigned_limitations:
            research_limitation = ResearchLimitations(
                limitation_id=limitation.limitation_id,
                research_id=research.research_id
            )
            research_limitations.append(research_limitation)

    return research_limitations


def generate_peer_expert_research_types(research_types: list[ResearchTypesModel], peer_experts: list[PeerExperts]):
    print_message("Generating user-organization relationships...")
    peer_expert_research_types = []

    research_type_count = len(research_types)
    for peer_expert in peer_experts:
        research_types: list[ResearchTypesModel] = random.sample(research_types, research_type_count)

        for research_type in research_types:
            peer_expert_research = PeerExpertsResearchTypes(
                peer_expert_id=peer_expert.peer_expert_id,
                research_type_id=research_type.research_type_id
            )
            peer_expert_research_types.append(peer_expert_research)

    return peer_expert_research_types


def generate_admin_account():
    print_message("Adding admin account...")

    salt = generate_salt()  # generate salt

    return [Users(
        first_name="admin",
        last_name="",
        email="admin",
        phone_number=-1,
        password=hash_password("admin", salt),
        salt=salt,
    )]


def set_accounts_admin(accounts: list[Users]):
    print_message("Adding admin permissions to accounts...")
    admin_accounts = []
    for account in accounts:
        admin_accounts.append(UsersStichtingAccessibility(
            user_id=account.user_id,
            admin=True
        ))
    return admin_accounts


def add_credentials(fake: Faker, users: list[Users]):
    credentials = []

    for sample in users:
        password_str = fake.password()
        salt = generate_salt()
        sample.password = hash_password(password_str, salt)
        sample.salt = salt

        credentials.append({
            "login": sample.email,
            "password": password_str
        })

    return credentials


def generate_registrations(peer_experts: list[PeerExperts], fake_researches: list[Research],
                           registration_statuses: list[RegistrationStatus]):
    print_message("Generating research registrations...")
    registrations = []

    for expert in peer_experts:
        if random.random() < 0.5:  # 50% chance the user will have any registration
            registration_count = 1 if random.random() < 0.9 else 2
            researches_registered = random.sample(fake_researches, registration_count)

            for research in researches_registered:
                registration = PeerExpertRegistration(
                    registration_status_id=random.choice(registration_statuses).registration_status_id,
                    peer_expert_id=expert.peer_expert_id,
                    research_id=research.research_id
                )
                registrations.append(registration)

    return registrations


def init_db_data(amount_multiplier=1):
    # Drop all tables and create new ones
    print_message("Dropping existing tables...")
    db.drop_all()
    print_message("Creating tables...")
    db.create_all()
    print_message("✅ Initialized database.")

    # Generate admin account
    admin_account = generate_admin_account()
    db.session.bulk_save_objects(admin_account, return_defaults=True)

    admin_account_stichting_accessibility = set_accounts_admin(admin_account)
    db.session.bulk_save_objects(admin_account_stichting_accessibility)

    # Generate fake data
    fake = Faker(['nl_NL', 'nl_BE', 'fr_FR', 'en_GB'])

    fake_users = generate_dummy_users(fake, amount_multiplier)
    db.session.bulk_save_objects(fake_users, return_defaults=True)

    random.shuffle(fake_users)

    # Move the first 5 elements to 'peers' and remove them from 'fake_users'
    peers = fake_users[:5]
    fake_users = fake_users[5:]

    # Move the next 5 elements to 'company' and remove them from 'fake_users'
    company = fake_users[:5]
    fake_users = fake_users[5:]

    with open('credentials.json', 'w') as f:
        credentials_peers = add_credentials(fake, peers)
        for credential in credentials_peers:
            credential["role"] = "peer"

        credentials_company = add_credentials(fake, company)
        for credential in credentials_company:
            credential["role"] = "company"

        json.dump([*credentials_peers, *credentials_company], f, indent=4)

    # Save the edited users to the database
    db.session.add_all(peers)  # Add the peers to the session
    db.session.add_all(company)  # Add the company users to the session

    organization_types = generate_organization_types()
    db.session.bulk_save_objects(organization_types, return_defaults=True)

    fake_organizations = generate_dummy_organizations(fake, organization_types, amount_multiplier)
    db.session.bulk_save_objects(fake_organizations, return_defaults=True)

    user_organizations = generate_user_organization_relationships(fake_users, fake_organizations, company)
    db.session.bulk_save_objects(user_organizations, return_defaults=True)

    limitations = generate_limitations()
    db.session.bulk_save_objects(limitations, return_defaults=True)

    limitations_lookup = {limitation.limitation_id: limitation for limitation in limitations}

    contact_preferences = generate_contact_preferences()
    db.session.bulk_save_objects(contact_preferences, return_defaults=True)

    peer_expert_statuses = generate_peer_expert_statuses()
    db.session.bulk_save_objects(peer_expert_statuses, return_defaults=True)

    peer_experts = generate_peer_experts(fake, user_organizations, fake_users, contact_preferences,
                                         peer_expert_statuses, peers)
    db.session.bulk_save_objects(peer_experts, return_defaults=True)

    peer_experts_limitations = generate_peer_experts_limitations(peer_experts, limitations)
    db.session.bulk_save_objects(peer_experts_limitations)

    research_statuses = generate_research_statuses()
    research_types = generate_research_types()
    db.session.bulk_save_objects([*research_statuses, *research_types], return_defaults=True)

    fake_researches = generate_researches(fake, research_statuses, research_types, amount_multiplier)
    fake_researches = [*get_researches(limitations_lookup), *fake_researches]
    db.session.bulk_save_objects(fake_researches, return_defaults=True)

    peer_experts_research_types = generate_peer_expert_research_types(research_types, peer_experts)
    db.session.bulk_save_objects(peer_experts_research_types)

    registration_statuses = generate_registration_statuses()
    db.session.bulk_save_objects(registration_statuses, return_defaults=True)

    registrations = generate_registrations(peer_experts, fake_researches, registration_statuses)
    db.session.bulk_save_objects(registrations)

    api_keys = generate_api_keys()
    db.session.bulk_save_objects(api_keys)

    db.session.commit()  # Save data

    return "✅ Added dummy data to database"