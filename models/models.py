from extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100), unique=True)

    phone = db.Column(db.String(15))

    password = db.Column(db.String(200))

    role = db.Column(db.String(50))

    address = db.Column(db.String(300))


class Service(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    category = db.Column(db.String(100))

    description = db.Column(db.Text)

    price = db.Column(db.Integer)


class Booking(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    service_id = db.Column(db.Integer)

    provider_id = db.Column(db.Integer)

    booking_date = db.Column(db.String(100))

    booking_time = db.Column(db.String(100))

    problem_description = db.Column(db.Text)

    status = db.Column(db.String(50), default='Pending')