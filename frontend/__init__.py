from flask import Flask, render_template

# Create flask instance
app = Flask(__name__)

# Config flask application
app.config['SECRET_KEY'] = "dev"

@app.route('/')
def main():
    return render_template("index.html")

# run the app (don't forget to set debug=False when the app is done)
if __name__ == "__main__":
    app.run(debug=True)
