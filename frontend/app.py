from flask import render_template, request, redirect, url_for, flash
from backend import create_app, db
from backend.database.models.register_expert import ExpertRegistrationModule


app = create_app()

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('peer_register.html')
    elif request.method == 'POST':
        form_data = request.form  # Haalt alle gegevens op uit het HTML-formulier
        registration = ExpertRegistrationModule()
        if registration.register_expert(form_data):
            flash('Registratie succesvol!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Er is een fout opgetreden tijdens de registratie.', 'danger')
            return render_template('peer_register.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
