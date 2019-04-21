from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager()

class User(db.Model):
    __tablename__='user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    address = db.Column(db.String(128), nullable=False)
    reviews = db.relationship('Review', backref='review', lazy=True)


    def __init__(self, name, email, password,address):
        self.name = name
        self.email = email
        self.password = self.__generate_hash(password)
        self.address = address

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def __repr(self):
        return '<id {}>'.format(self.id)

class Review(db.Model):
    __tablename__='review'
    id = db.Column(db.Integer(),primary_key=True)
    book_title= db.Column(db.String(255), nullable=False)
    reviews= db.Column(db.String(255), nullable=False)
    rating= db.Column(db.Integer())
    review_id= db.Column(db.Integer, db.ForeignKey('review.id'),
    nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(id, self.book_title)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
