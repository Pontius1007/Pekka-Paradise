from app import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(15), db.foreignKey(''))

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return '<User %r>' % self.user_id


class Course(db.Model):
    course_id = db.Column(db.String(10), primary_key=True)
    course_name = db.Column(db.String(50), unique=True)

    def __init__(self, course_id):
        self.course_id = course_id

    def __repr__(self):
        return '<Course %r>' % self.course_id
