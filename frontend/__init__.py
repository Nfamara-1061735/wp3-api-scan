import os

from flask import render_template, request, g, Blueprint, Flask, redirect, url_for, flash
from backend.database.models.register_expert import ExpertRegistrationModule

template_dir = os.path.abspath('./frontend/templates/')
static_dir = os.path.abspath('./frontend/static/')

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
def peer_home():
    return render_template("peer_home.jinja", theme=g.theme)


@frontend_bp.route('/peer/register', methods=['GET', 'POST'])
def register():
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


@frontend_bp.route('/peer/signin')
def signup():
    return render_template("sign_in.jinja", theme=g.theme)


@frontend_bp.route('/admin/dashboard')
def dashboard():
    return render_template("admin_dashboard.jinja", theme=g.theme)


@frontend_bp.route('/peer/dashboard', methods=['GET', 'POST'])
def peer_dashboard():
    return render_template("peer_dashboard.jinja", theme=g.theme)


@frontend_bp.route('/docs')
def documentation():
    return render_template("api_documentation.jinja", theme=g.theme)