# from werkzeug.security import generate_password_hash
from datetime import datetime
from backend import db
from backend.database.models.peer_experts_model import PeerExperts

class ExpertRegistrationModule:
    def __init__(self):
        pass

    def register_expert(self, form_data):
        try:
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
                user_id=form_data.get('user_id')
            )