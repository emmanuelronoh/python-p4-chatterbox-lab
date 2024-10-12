from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Create the Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Adjust as needed
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import your models here to avoid circular imports
    with app.app_context():
        from .models import Message  # Adjust as needed
    
    # Register blueprints if you have any
    # from .your_blueprint import your_blueprint
    # app.register_blueprint(your_blueprint)

    return app

# For running the app directly (if needed)
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
