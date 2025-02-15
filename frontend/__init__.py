from flask import Flask, render_template

# Create flask instance
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

# Config flask application
app.config['SECRET_KEY'] = "dev"

@app.route('/')
def main():
    return render_template("home.html")

# run the app (don't forget to set debug=False when the app is done)
if __name__ == "__main__":
    app.run(debug=True)
