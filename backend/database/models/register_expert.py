from datetime import datetime
from backend import db
from backend.database.models.peer_experts_model import PeerExperts
from backend.database.models.users_model import Users  # Toegevoegd voor user-model
from backend.utils.password import generate_salt, hash_password  # Voor password hashing

class ExpertRegistrationModule:
    def __init__(self):
        pass

    def register_expert(self, form_data):
        try:
            # Stap 1: Maak eerst de nieuwe gebruiker aan
            salt = generate_salt()
            hashed_password = hash_password(form_data.get('password'), salt)

            new_user = Users(
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                email=form_data.get('email_adress'),
                phone_number=form_data.get('telefoon_nummer'),
                password=hashed_password,
                salt=salt
            )

            db.session.add(new_user)
            db.session.flush()  # Genereert nieuwe user_id voordat je commit

            expert = PeerExperts(
                postal_code=form_data.get('postal_code'),
                gender=form_data.get('gender'),
                birth_date=datetime.strptime(form_data.get('birth_date'), '%Y-%m-%d').date(),
                tools_used=form_data.get('tools_used'),
                short_bio=form_data.get('short_bio'),
                special_notes=form_data.get('special_notes'),
                accepted_terms='accepted_terms' in form_data,
                has_supervisor='has_supervisor' in form_data,
                supervisor_or_guardian_name=form_data.get('supervisor_or_guardian_name'),
                availability_notes=form_data.get('availability_notes'),
                contact_preference_id=form_data.get('contact_preference_id'),
                user_id=form_data.get('user_id'),
                peer_expert_status_id = form_data.get('peer_expert_status_id', 1)
            )
            db.session.add(expert)
            db.session.commit()
            print("Nieuwe ervaringsdeskundige succesvol toegevoegd aan de database.")
            return True

        except Exception as e:
            db.session.rollback()
            print(f"Er is een fout opgetreden tijdens registratie: {str(e)}")
            return False