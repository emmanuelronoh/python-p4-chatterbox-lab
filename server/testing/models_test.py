import pytest
from datetime import datetime
from server.app import app, db
from models import Message

@pytest.fixture(scope='module')
def test_client():
    """Create a test client for the app."""
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables before tests
            yield client  # This is where the testing happens
            db.drop_all()  # Clean up after tests

@pytest.fixture(autouse=True)
def clean_database():
    """Clear the database before each test."""
    with app.app_context():
        db.session.remove()  # Remove any existing sessions
        db.drop_all()  # Drop all tables to start fresh
        db.create_all()  # Create tables for the new test
        yield  # This is where the testing happens
        db.session.remove()  # Clean up the session

class TestMessage:
    '''Message model in models.py'''

    def test_has_correct_columns(self, test_client):
        '''Test that the Message model has the correct columns.'''
        hello_from_liza = Message(body="Hello 👋", username="Liza")
        db.session.add(hello_from_liza)
        db.session.commit()

        assert hello_from_liza.body == "Hello 👋"
        assert hello_from_liza.username == "Liza"
        assert isinstance(hello_from_liza.created_at, datetime)

    def test_creates_new_message(self, test_client):
        '''Test creating a new message in the database.'''
        hello_from_liza = Message(body="Hello 👋", username="Liza")
        db.session.add(hello_from_liza)
        db.session.commit()

        # Verify the message was added to the database
        retrieved_message = Message.query.filter_by(body="Hello 👋", username="Liza").first()
        assert retrieved_message is not None
        assert retrieved_message.body == hello_from_liza.body
        assert retrieved_message.username == hello_from_liza.username

    def test_deletes_message(self, test_client):
        '''Test deleting a message from the database.'''
        hello_from_liza = Message(body="Hello 👋", username="Liza")
        db.session.add(hello_from_liza)
        db.session.commit()

        db.session.delete(hello_from_liza)
        db.session.commit()

        assert Message.query.filter_by(body="Hello 👋").first() is None

    def test_updates_message(self, test_client):
        '''Test updating a message in the database.'''
        message = Message(body="Old Message", username="Liza")
        db.session.add(message)
        db.session.commit()

        # Update the message
        message.body = "Updated Message"
        db.session.commit()

        updated_message = Message.query.get(message.id)
        assert updated_message.body == "Updated Message"
