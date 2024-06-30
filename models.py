from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


from ext import db, login_manager



class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    @staticmethod
    def save():
        db.session.commit()


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    img = db.Column(db.String(), nullable=False, default="default_photo.jpg")



class User(db.Model, BaseModel, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.String())
    
    def __init__(self, username, password, role="Guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class ContactMessage(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    email = db.Column(db.String())
    message = db.Column(db.Text)
