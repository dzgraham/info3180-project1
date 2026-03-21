from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate

# Create app directly (NOT using factory pattern)
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions directly with app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to add or view properties.'

# Import views and models at the end
from app import views, models

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return models.UserProfile.query.get(int(user_id))