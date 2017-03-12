from app import db
from sqlalchemy import PrimaryKeyConstraint


class UserFacebook(db.Model):
    __tablename__ = 'userfacebook'
    user_id = db.Column(db.String(100), primary_key=True)
    subject = db.Column(db.String(20), db.ForeignKey('subject.subject_id'))

    def __init__(self, user_id, subject_name):
        self.user_id = user_id
        self.subject = subject_name

    def __repr__(self):
        return '<User %r>' % self.user_id


class Subject(db.Model):
    __tablename__ = 'subject'
    subject_id = db.Column(db.String(20), primary_key=True)

    def __init__(self, subject_id):
        self.subject_id = subject_id

    def __repr__(self):
        return '<Subject %r>' % self.subject_id


class Lecture(db.Model):
    __tablename__ = 'lecture'
    subject = db.Column(db.String(20), db.ForeignKey('subject.subject_id'), primary_key=True)
    date = db.Column(db.String(10), primary_key=True)
    day_number = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(5), primary_key=True)
    end_time = db.Column(db.String(5))
    room_name = db.Column(db.String(5), primary_key=True)
    PrimaryKeyConstraint(subject, date, day_number, start_time, room_name)

    def __init__(self, subject, date, day_number, start_time, end_time, room_name):
        self.subject = subject
        self.date = date
        self.day_number = day_number
        self.start_time = start_time
        self.end_time = end_time
        self.room_name = room_name

    def __repr__(self):
        return '<Lecture %r>' % self.date


class LectureFeedback(db.Model):
    __tablename__ = 'lecturefeed'
    user_id = db.Column(db.String(100), primary_key=True)
    feedback = db.Column(db.String(50))
    subject = db.Column(db.String(20))

    def __init__(self, user_id, subject_name, feedback):
        self.user_id = user_id
        self.subject = subject_name
        self.feedback = feedback

    def __repr__(self):
        return '<Feedback %r>' % self.user_id