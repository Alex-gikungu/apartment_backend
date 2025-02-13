# app.py

from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import routes_blueprint
from config import Config

# Initialize the Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object(Config)

# Initialize the database with the app
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register the routes Blueprint
app.register_blueprint(routes_blueprint)

# Create the database tables (if they don't exist)
with app.app_context():
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)