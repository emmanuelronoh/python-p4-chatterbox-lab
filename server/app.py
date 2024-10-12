#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from .models import db, Message

app = Flask(__name__)
CORS(app)  # Enable CORS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    """Home route for the API."""
    return '<h1>Message API</h1>'

@app.route('/messages', methods=['GET'])
def get_messages():
    """Returns an array of all messages as JSON, ordered by created_at in ascending order."""
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return make_response(jsonify([message.to_dict() for message in messages]), 200)

@app.route('/messages', methods=['POST'])
def create_message():
    """Creates a new message with a body and username, and returns the created message as JSON."""
    data = request.get_json()

    if not data or 'body' not in data or 'username' not in data:
        return make_response(jsonify({"error": "Invalid input"}), 400)

    new_message = Message(body=data['body'], username=data['username'])
    
    db.session.add(new_message)
    db.session.commit()
    
    return make_response(new_message.to_dict(), 201)

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    """Updates the body of the message and returns the updated message as JSON."""
    message = Message.query.get_or_404(id)
    data = request.get_json()

    if 'body' in data:
        message.body = data['body']
        
    db.session.commit()
    
    return make_response(message.to_dict(), 200)

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    """Deletes the message from the database and returns a confirmation message."""
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    
    return make_response(jsonify({"message": "Message deleted successfully."}), 204)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
