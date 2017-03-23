from app import db, models
import datetime
import lecture_methods


def add_entry(user_name, subject_name, feedback):
    """
    add feedback to lecturefeedback-table if feedback has not already been given by the user for the active lecture.
    :param user_name:
    :param subject_name:
    :param feedback:
    :return: True or False
    """
    date = datetime.date.today()
    year = date.year
    week = datetime.date.isocalendar(date)[1]
    weekday = datetime.datetime.today().weekday() + 1
    lectures = models.Lecture.query.filter_by(subject=subject_name, year=year,
                                              week_number=week, day_number=weekday)
    try:
        if lectures.count() > 0:
            if user_has_feedback_for_lecture(user_name, lectures[0]):
                # Reject feedback
                return False
            else:
                # Store feedback
                feedback = models.LectureFeedback(user_name, feedback, lectures[0].id)
                db.session.add(feedback)
                db.session.commit()
                return True
    except Exception as e:
        print('Error:')
        print(e)
    # Reject feedback
    return False


def get_all_subject_feed(subject):
    """
    :param subject:
    :return: List [subject, feed1, feed2, feed3]
    """
    ids = lecture_methods.get_lectures_from_subject(subject)
    feedback_list = [subject]
    if len(ids) > 0:
        for lec_id in ids:
            for feedback in models.LectureFeedback.query.filter_by(lecture_id=lec_id):
                feedback_list.append(feedback.feedback)
    return feedback_list


def user_has_feedback_for_lecture(user_name, lecture):
    """
    Checks if user has already given feedback for a lecture.
    :param user_name:
    :param lecture:
    """
    try:
        return models.LectureFeedback.query.filter_by(user_id=user_name, lecture_id=lecture.id).count() > 0
    except Exception as e:
        print(e)
    return False

