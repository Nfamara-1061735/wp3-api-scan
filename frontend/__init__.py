import os

from flask import render_template, request, g, Blueprint, redirect, url_for, flash
from flask import session

from backend.api.api import SingleResearch, FilteredPeerExpertRegistrations, FilteredPeerExperts
from backend.api.researches import FilteredResearch
from backend.database.models.register_expert import ExpertRegistrationModule
from backend.utils.check_permissions import check_permission

template_dir = os.path.abspath('./frontend/templates/')
static_dir = os.path.abspath('./frontend/static/')
singleResearch = SingleResearch()
filteredResearch = FilteredResearch()
filteredPeerExpertRegistrations = FilteredPeerExpertRegistrations()
filteredPeerExperts = FilteredPeerExperts()

# Define the frontend blueprint
frontend_bp = Blueprint('frontend', __name__, template_folder=template_dir, static_folder=static_dir,
                        static_url_path='/static/frontend')

@frontend_bp.before_request
def before_request():
    """
    Runs before the main route function
    """
    g.theme = request.cookies.get('theme', 'light')  # 'g' is a temporary request specific value

@frontend_bp.route('/')
def home():
    print(os.listdir(frontend_bp.static_folder))
    return render_template("home.jinja", theme=g.theme)


@frontend_bp.route('/peer/home')
@check_permission('peer')
def peer_home():
    if g.get('user', None):
        return redirect(url_for("frontend.peer_dashboard"))
    return render_template("peer_home.jinja", theme=g.theme)


@frontend_bp.route('/peer/register', methods=['GET', 'POST'])
@check_permission('peer')
def register():
    if g.get('user', None):
        return redirect(url_for("frontend.peer_dashboard"))
    if request.method == 'GET':
        return render_template('peer_register.html', theme=g.theme)
    elif request.method == 'POST':
        form_data = request.form  # Haalt alle gegevens op uit het HTML-formulier
        registration = ExpertRegistrationModule()
        if registration.register_expert(form_data):
            flash('Registratie succesvol!', 'success')
            return redirect(url_for('frontend.peer_home'))
        else:
            flash('Er is een fout opgetreden tijdens de registratie.', 'danger')
            return render_template('peer_register.html')


@frontend_bp.route('/logout')
def logout():
    if "user" in session:
        del session["user"]
    return redirect(url_for('frontend.home'))

@frontend_bp.route('/peer/signin')
@check_permission('peer')
def signup():
    if g.get('user', None):
        return redirect(url_for("frontend.peer_dashboard"))
    return render_template("sign_in.jinja", role='peer', target_redirect=url_for("frontend.peer_dashboard"),
                           theme=g.theme)


@frontend_bp.route('/admin/signin')
@check_permission('admin')
def login_admin():
    if g.get('user', None):
        return redirect(url_for("frontend.dashboard"))
    return render_template("sign_in.jinja", role='admin', target_redirect=url_for("frontend.dashboard"), theme=g.theme)

@frontend_bp.route('/admin/dashboard')
@check_permission('admin')
def dashboard():
    if not g.get('user', None):
        return redirect(url_for("frontend.login_admin"))
    if request.method == 'GET':
        return render_template("admin_dashboard.jinja", theme=g.theme, researches=filteredResearch.get(1))

#The routes below is a TEST-ROUTE. FOR TESTING PURPOSES ONLY!
@frontend_bp.route('/peer_experts')
def peer_experts():
    if request.method == 'GET':
        return filteredPeerExperts.get(1)

@frontend_bp.route('/peer_expert_registrations')
def peer_expert_registrations():
    if request.method == 'GET':
        return filteredPeerExpertRegistrations.get(1)

@frontend_bp.route('/dashboard_data')
def researches():
    if request.method == 'GET':
        return filteredResearch.get(1)
    if request.method == 'PATCH':
        data = request.get_json()
        research_data = data['research']

        item_id = research_data['item_id']
        updated_status = research_data['updated_status']

        if not item_id:
            return {"message": "Item not found"}, 404
        if not updated_status:
            return {"message": "Update id invalid"}, 404

        return filteredResearch.patch(updated_status, item_id), 200

@frontend_bp.route('/peer/dashboard', methods=['GET', 'POST'])
@check_permission('peer')
def peer_dashboard():
    if not g.get('user', None):
        return redirect(url_for("frontend.peer_home"))
    return render_template("peer_dashboard.jinja", theme=g.theme)


@frontend_bp.route('/docs', methods=['GET', 'POST'])
def documentation():
    return render_template("api_documentation.jinja", theme=g.theme)