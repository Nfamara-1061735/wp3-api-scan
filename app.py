from flask import Flask, render_template

# Create flask instance
app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

# Config flask application
app.config['SECRET_KEY'] = "dev"

@app.route('/')
def main():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True) 