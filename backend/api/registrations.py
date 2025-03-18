from flask import session, g
from flask_restful import Resource, abort

from backend.database.models import PeerExpertRegistration
from backend.utils.check_permissions import check_permission


class Registrations(Resource):
    @check_permission('peer')
    def get(self):
        if not 'user' in session or not session['user'].peer_expert_info:
            abort(403)

        user = g.user

        registrations: PeerExpertRegistration
        pass
