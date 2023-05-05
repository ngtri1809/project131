from datetime import datetime
from flask_login import LoginManager, UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

#User object
class User(db.Model, UserMixin):
    #primary key is like a unique identifier for each row
    id = db.Column(db.Integer, primary_key=True)
    #Size (32), nullable is to see if the column is empty or not. false means can't be empty
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    #bug here
    #friends = db.relationship('Friengit add', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    #each function inside of a database has to have self parameter
    def __repr__(self):
        return f'<user {self.id}: {self.username}>'
    
    def received_messages(self):
        return Message.query.filter_by(recipient=self).order_by(Message.timestamp.desc()).all()
class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #bug here
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #friend_of = db.relationship('User', foreign_keys=[user_id])

    def __repr__(self):
        return f"Friend('{self.name}', '{self.email}')"
    
#Message object
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())

    sender = db.relationship('User', foreign_keys=[sender_id])
    recipient = db.relationship('User', foreign_keys=[recipient_id])

class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # set the foreign key from user
    name = db.Column(db.String(100)) # name of the task
    done = db.Column(db.Boolean) #user mark as done or undone
    #Define relationship between user and todo list's tasks using the user_id 
    user = db.relationship('User', foreign_keys=[user_id])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
