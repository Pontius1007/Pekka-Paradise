from app import db, models
import datetime


def add_entry(user_name, subject_name, feedback):
    """
    add feedback to lecturefeedback-table if feedback has not already been given by the user for the active lecture.
    :param user_name: 
    :param subject_name:
    :param feedback:
    """
    date = datetime.date.today()
    year = date.year
    week = datetime.date.isocalendar(date)[1]
    weekday = datetime.datetime.today().weekday() + 1
    lectures = models.Lecture.query.filter_by(subject=subject_name, year=year,
                                              week_number=week, day_number=weekday).count()
    try:
        if lectures > 0:
            if user_has_feedback_for_lecture(user_name, lectures[0]):
                # Reject feedback
                return False
            else:
                # Store feedback
                feedback = models.LectureFeedback(user_name, feedback, lectures.id)
                db.session.add(feedback)
                db.session.commit()
                return True
    except Exception as e:
        print(e)
    # Reject feedback
    return False


# TODO Fix this
def user_has_feedback_for_lecture(user_name, lecture):
    try:
        return models.LectureFeedback.query.filter_by(user_id=user_name, lecture_id=lecture.id) > 0
    except Exception as e:
        print(e)
    return False
