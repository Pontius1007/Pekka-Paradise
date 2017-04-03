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
    feedback_list = []
    feedbackevaluation_list = []
    if len(ids) > 0:
        for lec_id in ids:
            for feedback in models.LectureFeedback.query.filter_by(lecture_id=lec_id):
                feedback_list.append(int(feedback.feedback))
            for feedbackevaluation in models.LectureFeedbackEvaluation.query.filter_by(lecture_id=lec_id):
                feedbackevaluation_list.append([feedbackevaluation.increased_knowledge,
                                                feedbackevaluation.well_organized, feedbackevaluation.logical,
                                                feedbackevaluation.use_of_slides, feedbackevaluation.use_of_time,
                                                feedbackevaluation.presenter_knowledgeable,
                                                feedbackevaluation.general_score])
    return feedback_list, feedbackevaluation_list


def get_single_lecture_feed(year, week, day, subject):
    """
    Gets all the feedback from a single lecture.
    :param year: int
    :param week: int
    :param day: int
    :param subject string
    :return: feedback_list[lecture_id, list[int]], feedback_question_list[]
    """
    lecture_id = lecture_methods.get_lecture_from_date(year, week, day, subject)
    feedback_list = []
    return_list = [lecture_id, feedback_list]
    for feedback in models.LectureFeedback.query.filter_by(lecture_id=lecture_id):
        feedback_list.append(int(feedback.feedback))

    return return_list


def get_single_lecture_feedback_questions(year, week, day, subject):
    """
    Gets all the feedbacks from a single lecture from the LectureFeedbackEvaluation table.
    :param year: int
    :param week: int
    :param day: int
    :param subject: String
    :return: 
    """
    lecture_id = lecture_methods.get_lecture_from_date(year, week, day, subject)
    feedback_question_list = []
    for feedback in models.LectureFeedbackEvaluation.query.filter_by(lecture_id=lecture_id):
        feedback_question_list.append([feedback.increased_knowledge, feedback.well_organized, feedback.logical,
                                       feedback.use_of_slides, feedback.use_of_time, feedback.presenter_knowledgeable,
                                       feedback.general_score])
    return feedback_question_list



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
    :return: Boolean
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
    # Reject feedback
    return False


def user_can_give_feedback_evaluation(user_name, subject_name):
    """
    Check if user can give feedback to the LectureFeedbackEvaluation table.
    :param user_name: String
    :param subject_name: String
    :return: Boolean
    """
    today = get_today()
    lectures = models.Lecture.query.filter_by(subject=subject_name, year=today[0],
                                              week_number=today[1], day_number=today[2])
    if lectures.count() > 0:
        for lecture in lectures:
            print(lecture)
            if user_has_feedback_for_lecture_evaluation(user_name, lecture):
                # User has already given feedback
                return False
        return True
    else:
        print('no lecture')
        # There are no lectures for this subject.
        return False
    pass


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


def remove_all_feedback(user_name):
    """
    This method is only used for testing and removes
    test data from database
    :param user_name: 
    :return: 
    """
    for row in models.LectureFeedback.query.filter_by(user_id=user_name):
        db.session.delete(row)
    # db.session.delete(models.LectureFeedback.query.get(user_name))
    # Remove the other feedback thingy
    db.session.commit()


def get_day():
    """
    :return day:
    """
    return datetime.datetime.today().weekday() + 1


def get_week():
    """
    :return week:
    """
    date = datetime.date.today()
    return datetime.date.isocalendar(date)[1]


def get_year():
    """
    :return year:
    """
    date = datetime.date.today()
    return date.year


def get_lecture_object(lecture_id):
    """
    :param lecture_id:
    :return true or false:
    """
    try:
        return models.Lecture.query.get(lecture_id)
    except Exception as e:
        print(e)

