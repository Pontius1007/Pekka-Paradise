import datetime

import lecture_methods
from app import db, models


def add_entry(user_name, subject_name, feedback):
    """
    add feedback to lecturefeedback-table if feedback has not already been given by the user for the active lecture.
    :param user_name:
    :param subject_name:
    :param feedback:
    :return: True or False
    """
    today = get_today()
    lectures = models.Lecture.query.filter_by(subject=subject_name, year=today[0],
                                              week_number=today[1], day_number=today[2])
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
                feedback_list.append(int(feedback.feedback))
    return feedback_list


def get_single_lecture_feed(year, week, day):
    """
    Gets all the feedbacks from a single lecture.
    :param year: int
    :param week: int
    :param day: int
    :return: list[lecture_id, list[int]]
    """
    lecture_id = lecture_methods.get_lecture_from_date(year, week, day)
    feedback_list = []
    return_list = [lecture_id, feedback_list]
    for feedback in models.LectureFeedback.query.filter_by(lecture_id=lecture_id):
        feedback_list.append(int(feedback.feedback))
    return return_list


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


def add_feedback_evaluation(user_name, subject_name, increased_knowledge, well_organized, logical, use_of_slides,
                            use_of_time, presenter_knowledgeable, general_score):
    """
    Takes in scores and makes a lecturefeedbackevaluation adn stores in database. 
    :param user_name: 
    :param subject_name: 
    :param increased_knowledge: 
    :param well_organized: 
    :param logical: 
    :param use_of_slides: 
    :param use_of_time: 
    :param presenter_knowledgeable: 
    :param general_score: 
    :return: 
    """
    today = get_today()
    lectures = models.Lecture.query.filter_by(subject=subject_name, year=today[0],
                                              week_number=today[1], day_number=today[2])
    if lectures.count() > 0:
        if user_has_feedback_for_lecture_evaluation(user_name, lectures[0]):
            # Reject feedback
            return False
        else:
            try:
                feedback = models.LectureFeedbackEvaluation(user_name, lectures[0].id, increased_knowledge,
                                                            well_organized, logical, use_of_slides, use_of_time,
                                                            presenter_knowledgeable, general_score)
                db.session.add(feedback)
                db.session.commit()
                return True
            except ValueError as e:
                print(e)
    # Rejact feedback
    return False


def user_has_feedback_for_lecture_evaluation(user_name, lecture):
    """
    Checks if user has already given feedbackevaluation for a lecture.
    :param user_name:
    :param lecture:
    """
    try:
        return models.LectureFeedbackEvaluation.query.filter_by(user_id=user_name, lecture_id=lecture.id).count() > 0
    except Exception as e:
        print(e)
    return False


def get_today():
    """
    Returns year, week and day.
    :return: [year, week, day]
    """
    date = datetime.date.today()
    return [date.year, datetime.date.isocalendar(date)[1], datetime.datetime.today().weekday() + 1]
