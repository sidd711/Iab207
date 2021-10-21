from sqlalchemy.orm import backref
from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    # password is never stored in the DB, an encrypted password is stored
    # the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)
    contact_no = db.Column(db.String(25), nullable=False)
    image = db.Column(
        db.String(400), default="Website\\static\\images\\user_imgs\\profile.png")

    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='users')
    bookings = db.relationship('Booking', backref='users')


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    startdate = db.Column(db.Date, nullable=False)
    enddate = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    starttime = db.Column(db.Time, nullable=False)
    endtime = db.Column(db.Time, nullable=False)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String(80))
    suburb = db.Column(db.String(80))
    # wanna figure out how to max this
    maxguests = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(400))
    type = db.Column(db.String(80))
    description = db.Column(db.String(200))
    description_header = db.Column(db.String(100))
    artist = db.Column(db.String(80), nullable=False)
    # ... Create the Comments db.relationship
    # relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='events')
    # add a fk to tie the currently logged in user to the even
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    name = db.relationship('User', backref='events')

    def __repr__(self):  # string print method
        return "<Name: {}>".format(self.name)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.Date, default=datetime.now())
    # add the foreign keys
    user = db.Column(db.Integer, db.ForeignKey('users.name'))

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Comment: {}>".format(self.text)


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    # A booking needs a date
    created_at = db.Column(db.Date, default=datetime.now())
    # add the foreign keys
    # A booking needs to be for a user
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    # A booking needs to be for an event
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    # It is helpful for the booking to feature the event date
    event_date = db.Column(db.Integer, db.ForeignKey('events.startdate'))

    def __repr__(self):
        return "<Comment: {}>".format(self.text)
