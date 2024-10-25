from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
CORS(app)

# Configure your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

@app.before_first_request
def create_tables():
    """Create the database tables before the first request."""
    with app.app_context():
        db.create_all()

@app.route('/messages', methods=['GET'])
def get_messages():
    """Get all messages."""
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([{
        'id': m.id,
        'body': m.body,
        'username': m.username,
        'created_at': m.created_at,
        'updated_at': m.updated_at
    } for m in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    """Create a new message."""
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({
        'id': new_message.id,
        'body': new_message.body,
        'username': new_message.username,
        'created_at': new_message.created_at,
        'updated_at': new_message.updated_at
    }), 201  # Return HTTP 201 Created

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    """Update an existing message."""
    message = Message.query.get_or_404(id)
    data = request.get_json()
    message.body = data['body']
    db.session.commit()
    return jsonify({
        'id': message.id,
        'body': message.body,
        'username': message.username,
        'created_at': message.created_at,
        'updated_at': message.updated_at
    })

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    """Delete a message."""
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
