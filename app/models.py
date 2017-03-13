from app import db
from sqlalchemy import PrimaryKeyConstraint


class UserFacebook(db.Model):
    __tablename__ = 'userfacebook'
    user_id = db.Column(db.String(100), primary_key=True)
    subject = db.Column(db.String(20), db.ForeignKey('subject.subject_id'))

    def __init__(self, user_id, subject_name):
        self.user_id = user_id
        self.subject = subject_name.upper()

    def __repr__(self):
        return '<User %r>' % self.user_id


class Subject(db.Model):
    __tablename__ = 'subject'
    subject_id = db.Column(db.String(20), primary_key=True)

    def __init__(self, subject_id):
        self.subject_id = subject_id.upper()

    def __repr__(self):
        return '<Subject %r>' % self.subject_id


class Lecture(db.Model):
    __tablename__ = 'lecture'
    subject = db.Column(db.String(20), db.ForeignKey('subject.subject_id'), primary_key=True)
    year = db.Column(db.Integer, primary_key=True)  # Format YYYY
    week_number = db.Column(db.Integer, primary_key=True)  # Format: 1-52
    day_number = db.Column(db.Integer, primary_key=True)  # Format: int from 1-7
    start_time = db.Column(db.String(5), primary_key=True)  # Format: HH.MM
    end_time = db.Column(db.String(5))  # Format: HH.MM
    room_name = db.Column(db.String(5), primary_key=True)

    def __init__(self, subject, year, week_number, day_number, start_time, end_time, room_name):
        self.subject = subject.upper()
        self.year = year
        self.week_number = week_number
        self.day_number = day_number
        self.start_time = start_time
        self.end_time = end_time
        self.room_name = room_name

    def __repr__(self):
        return '<Lecture %r>' % self.week_number


class LectureFeedback(db.Model):
    __tablename__ = 'lecturefeed'
    user_id = db.Column(db.String(100), primary_key=True)
    feedback = db.Column(db.String(50))
    subject = db.Column(db.String(20))

    def __init__(self, user_id, subject_name, feedback):
        self.user_id = user_id
        self.subject = subject_name.upper()
        self.feedback = feedback

    def __repr__(self):
        return '<Feedback %r>' % self.user_id