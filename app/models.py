from app import db


class UserFacebook(db.Model):
    __tablename__ = 'userfacebook'
    user_id = db.Column(db.String(100), primary_key=True)
    subject = db.Column(db.String(20))

    def __init__(self, user_id, subject_name):
        self.user_id = user_id
        self.subject = subject_name

    def __repr__(self):
        return '<User %r>' % self.user_id


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
        return '<User %r>' % self.user_id
