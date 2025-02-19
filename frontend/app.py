from flask import Flask, render_template, request, redirect, url_for, flash
from backend import create_app,db
from backend.database.models.peer_experts_model import PeerExperts

# Create flask instance
app = create_app()

@app.route('/')
def main():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('peer_register.html')


@app.route('/admin')
def dashboard():
    return render_template("admin_dashboard.jinja")

# run the app (don't forget to set debug=False when the app is done)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
