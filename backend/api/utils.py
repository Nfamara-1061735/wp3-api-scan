from flask import jsonify, session, request

from backend.database.models.api_keys_model import ApiKeys

from functools import wraps

from backend import db


def method_not_allowed():
    response = jsonify({"error": "Methode niet toegestaan"})
    response.status_code = 405
    return response

# api-key validatie
def require_api_key(f):
   @wraps(f)
   def decorated_function(*args, **kwargs):
      print("🔍 Validatie gestart")  # Debug-print

      if session.get('user'):
         print("✅ Actieve sessie gevonden, API-key validatie overgeslagen")  # Debug-print
         return f(*args, **kwargs)

      print("❌ Geen actieve sessie gevonden, API-key validatie vereist\n")  # Debug-print
      print("🔍 Er wordt nu een API-key gezocht")  # Debug-print
      api_key_header = request.headers.get("Authorization")
      organization_name = request.headers.get("Organization-Name")

      if not api_key_header or not api_key_header.startswith("Bearer ") or not organization_name:
         print("❌ API-key of organisatie onjuist, validatie mislukt")  # Debug-print
         return {"error": "API-key of organisatie onjuist, validatie mislukt"}, 401

      api_key = api_key_header.split("Bearer ")[1]

      key_record = db.session.query(ApiKeys).filter_by(api_key=api_key).first()

      if not key_record or key_record.organization_name != organization_name:
         print(f"❌ Ongeldige API-key! voor organisatie: {organization_name}, validatie mislukt")  # Debug-print
         return {"error": "Ongeldige API-key voor deze organisatie, validatie mislukt"}, 401

      print(f"✅ API-key gevalideerd voor organisatie: {organization_name}")  # Debug-print
      return f(*args, **kwargs)

   return decorated_function