from flask import Flask

# Create flask instance
app = Flask(__name__)

# Config flask application
app.config['SECRET_KEY'] = "dev"

@app.route('/')
def main():
    return "welcome"