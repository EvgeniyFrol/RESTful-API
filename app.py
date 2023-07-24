from flask import Flask, request, jsonify, render_template, url_for, redirect
from peewee import IntegrityError

from models import User, Message, create_tables

app = Flask(__name__)


@app.route('/api/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        avatar = request.form.get('avatar')
        phone_number = request.form.get('phone_number')

        if not username or not password:
            return jsonify({'message': 'Username and password are required.'}), 400

        try:
            user = User.create(
                username=username,
                avatar=avatar,
                phone_number=phone_number,
                password=password
            )
            return jsonify({'message': 'Registration successful!'}), 201
        except IntegrityError:
            return jsonify({'message': 'Username already exists.'}), 400

    return render_template('register.html')


@app.route('/api/users/', methods=['GET'])
def search_users():
    query = request.args.get('query', '')
    users = User.select().where(User.username.contains(query))
    return render_template('users.html', users=users)


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.get_by_id(user_id)

        return render_template('user_detail.html', user=user)
    except User.DoesNotExist:
        return jsonify({'error': 'user not found'}), 404


@app.route('/api/chat', methods=['GET'])
def chat():
    users = User.select()
    messages = Message.select()
    return render_template('chat.html', users=users, messages=messages)


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    sender_id = int(request.form.get('sender_id'))
    content = request.form.get('content')

    try:
        sender = User.get_by_id(sender_id)
        message = Message.create(sender=sender, content=content)
        print(message)
        return jsonify({'message': 'Message sent successfully!'}), 201
    except User.DoesNotExist:
        return jsonify({'message': 'User not found.'}), 404


@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = Message.select().order_by(Message.timestamp)
    data = [{'sender': message.sender.username, 'content': message.content, 'time': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for message in messages]
    return jsonify({'messages': data})


if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=5000)