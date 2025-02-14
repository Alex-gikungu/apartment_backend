from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS  # Import CORS
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

# Enable CORS for specific origins and allow credentials
CORS(app, origins=["https://apartment-locator.vercel.app/"], supports_credentials=True)  # Configure CORS

# Register the routes Blueprint
app.register_blueprint(routes_blueprint)

# Create the database tables (if they don't exist)
with app.app_context():
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)