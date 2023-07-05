from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def get_messages():

    messages = []
    
    if request.method == 'GET':
        for message in Message.query.all():
            messages.append(message.to_dict())
        return make_response(messages, 200)

    elif request.method == 'POST':
        new_message_dict = request.get_json()
        new_message = Message(
            body=new_message_dict['body'],
            username=new_message_dict['username'],
        )

        db.session.add(new_message)
        db.session.commit()

        return make_response(new_message_dict, 201) 

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id = id).first()

    if message == None:
        response = {
            'message': 'No matching message in the database'
        }
        return make_response(response, 404)
    else:
        if request.method == 'PATCH':
            json_message = request.get_json()
            for attr in json_message:
                setattr(message, attr, json_message.get(attr))

                db.session.add(message)
                db.session.commit()

            return make_response(message.to_dict(), 200)
        
        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            return make_response(
                jsonify({'status': 'delete successful'}),
                200
            )


if __name__ == '__main__':
    app.run(port=5555)
