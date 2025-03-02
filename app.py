from flask import Flask, render_template, request, redirect, url_for, flash, g
from backend import create_app, db
from backend.database.models.peer_experts_model import PeerExperts

# Create flask instance
app = create_app()


@app.before_request
def before_request():
    """
    Runs before the main route function
    """
    g.theme = request.cookies.get('theme', 'light')  # 'g' is a temporary request specific value


@app.route('/')
def main():
    return render_template("home.jinja", theme=g.theme)


@app.route('/peer/home')
def peer_home():
    return render_template("peer_home.jinja", theme=g.theme)


@app.route('/peer/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('peer_register.html', theme=g.theme)


@app.route('/peer/signin')
def signup():
    return render_template("sign_in.jinja", theme=g.theme)


@app.route('/admin/dashboard')
def dashboard():
    return render_template("admin_dashboard.jinja", theme=g.theme)


@app.route('/peer/dashboard', methods=['GET', 'POST'])
def peer_dashboard():
    return render_template("peer_dashboard.jinja", theme=g.theme)

@app.route('/docs')
def documentation():
    return render_template("api_documentation.jinja", theme=g.theme)


# run the app (don't forget to set debug=False when the app is done)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
