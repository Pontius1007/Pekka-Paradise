from app import db


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
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(20), db.ForeignKey('subject.subject_id'))
    year = db.Column(db.Integer)  # Format YYYY
    week_number = db.Column(db.Integer)  # Format: 1-52
    day_number = db.Column(db.Integer)  # Format: int from 1-7
    start_time = db.Column(db.String(5))  # Format: HH.MM
    end_time = db.Column(db.String(5))  # Format: HH.MM
    room_name = db.Column(db.String(5))

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
    __tablename__ = 'lecturefeedback'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('userfacebook.user_id'))
    feedback = db.Column(db.String(15))
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))

    def __init__(self, user_id, feedback, lecture_id):
        self.user_id = user_id
        self.feedback = feedback
        self.lecture_id = lecture_id

    def __repr__(self):
        return '<Feedback %r>' % self.user_id


class LectureFeedbackEvaluation(db.Model):
    __tablename__ = 'lecturefeedbakevaluation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('userfacebook.user_id'))
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))
    # All the bellow are a score from 1 to 5.
    increased_knowledge = db.Column(db.Integer)
    well_organized = db.Column(db.Integer)
    logical = db.Column(db.Integer)
    use_of_slides = db.Column(db.Integer)
    use_of_time = db.Column(db.Integer)
    presenter_knowledgeable = db.Column(db.Integer)
    general_score = db.Column(db.Integer)

    def __init__(self, increased_knowledge, well_organized, logical, use_of_slides, use_of_time,
                 presenter_knowledgeable, general_score):
        if self.is_inside_bounds(increased_knowledge):
            self.increased_knowledge = increased_knowledge
        else:
            raise ValueError
        if self.is_inside_bounds(well_organized):
            self.well_organized = well_organized
        else:
            raise ValueError
        if self.is_inside_bounds(logical):
            self.logical = logical
        else:
            raise ValueError
        if self.is_inside_bounds(use_of_slides):
            self.use_of_slides = use_of_slides
        else:
            raise ValueError
        if self.is_inside_bounds(use_of_time):
            self.use_of_time = use_of_time
        else:
            raise ValueError
        if self.is_inside_bounds(presenter_knowledgeable):
            self.presenter_knowledgeable = presenter_knowledgeable
        else:
            raise ValueError
        if self.is_inside_bounds(general_score):
            self.general_score = general_score
        else:
            raise ValueError

    def is_inside_bounds(self, score):
        return 1 <= score <= 5