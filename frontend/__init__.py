from flask import render_template, request, g, Blueprint, Flask

# Define the frontend blueprint
frontend = Blueprint('frontend', __name__, static_folder='static', static_url_path='/static/')


@frontend.before_request
def before_request():
    """
    Runs before the main route function
    """
    g.theme = request.cookies.get('theme', 'light')  # 'g' is a temporary request specific value


@frontend.route('/')
def main():
    return render_template("home.jinja", theme=g.theme)


@frontend.route('/peer/home')
def peer_home():
    return render_template("peer_home.jinja", theme=g.theme)


@frontend.route('/peer/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('peer_register.html', theme=g.theme)


@frontend.route('/peer/signin')
def signup():
    return render_template("sign_in.jinja", theme=g.theme)


@frontend.route('/admin/dashboard')
def dashboard():
    return render_template("admin_dashboard.jinja", theme=g.theme)


@frontend.route('/peer/dashboard', methods=['GET', 'POST'])
def peer_dashboard():
    return render_template("peer_dashboard.jinja", theme=g.theme)


@frontend.route('/docs')
def documentation():
    return render_template("api_documentation.jinja", theme=g.theme)


def create_app():
    app = Flask(__name__)

    ## Register the frontend blueprint
    app.register_blueprint(frontend)
    return app


# Debug when running this script directly
# Use `flask --app frontend run` to run without debugging
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
