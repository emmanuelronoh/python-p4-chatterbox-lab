from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Initialize the SQLAlchemy object with a naming convention
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model):
    __tablename__ = 'messages'  # Table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    body = db.Column(db.String, nullable=False)    # Message body, cannot be null
    username = db.Column(db.String, nullable=False) # Username, cannot be null
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp of last update

    def __init__(self, body, username):
        self.body = body
        self.username = username

    def to_dict(self):
        """Convert the Message object to a dictionary."""
        return {
            'id': self.id,
            'body': self.body,
            'username': self.username,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()  # Include updated_at
        }

    def __repr__(self):
        return f'<Message {self.body} by {self.username}>'
