from datetime import datetime
from attendance import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Employee(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    designation = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    cardno = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=False)
    documents = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Employee('{self.id}', '{self.name}', '{self.phone}', '{self.email}', '{self.designation}', '{self.department}', '{self.cardno}', '{self.image_file}', '{self.documents}')"
    def __init__(self, id, name, phone, email, designation, department, cardno, image_file, documents):
        self.id = id
        self.name=name
        self.phone=phone
        self.email=email
        self.designation=designation
        self.department=department
        self.cardno=cardno
        self.image_file=image_file
        self.documents=documents


class Organization(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    department = db.Column(db.String(120), nullable=False)
    designation = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Organization('{self.department}', '{self.designation}')"

class Shift(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    Name = db.Column(db.String(40), nullable=False)
    SatartDate = db.Column(db.String(40))
    EndDate = db.Column(db.String(40))
    def __repr__(self):
        return f"Organization('{self.Name}', '{self.SatartDate}', '{self.EendDate}', '{self.Holidays}')"