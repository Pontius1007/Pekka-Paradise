from app import db, models
import datetime
import lecture_methods


def add_entry(user_name, subject_name, feedback):
    """
    add feedback to lecturefeedback-table if feedback has not already been given by the user for the active lecture.
    :param user_name: String
    :param subject_name: String
    :param feedback: String
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
    :param subject: String
    :return: feedback_list[feed1, feed2, feed3], feedbackevaluation_list[lecture_feedback[int]] there are 7 entries in
    each lecture_feedback
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
                                                feedbackevaluation.well_organized,
                                                feedbackevaluation.use_of_slides, feedbackevaluation.use_of_time,
                                                feedbackevaluation.presenter_knowledgeable,
                                                feedbackevaluation.general_score, feedbackevaluation.next_lecture])
    return feedback_list, feedbackevaluation_list


def get_single_lecture_feed(year, week, day, subject):
    """
    Gets all the feedbacks from a single lecture.
    :param year: int
    :param week: int
    :param day: int
    :param subject string
    :return: feedback_list[lecture_id, list[int]]
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
        feedback_question_list.append([feedback.increased_knowledge, feedback.well_organized,
                                       feedback.use_of_slides, feedback.use_of_time, feedback.presenter_knowledgeable,
                                       feedback.general_score, feedback.next_lecture])
    return feedback_question_list


def user_has_feedback_for_lecture(user_name, lecture):
    """
    Checks if user has already given feedback for a lecture.
    :param user_name: String
    :param lecture: int
    """
    try:
        return models.LectureFeedback.query.filter_by(user_id=user_name, lecture_id=lecture.id).count() > 0
    except Exception as e:
        print(e)
    return False


def add_feedback_evaluation(user_name, subject_name, increased_knowledge, well_organized, use_of_slides,
                            use_of_time, presenter_knowledgeable, general_score, next_lecture):
    """
    Takes in scores and makes a lecturefeedbackevaluation and stores in database.
    :param user_name: String
    :param subject_name: String
    :param increased_knowledge: int
    :param well_organized: int
    :param use_of_slides: int
    :param use_of_time: int
    :param presenter_knowledgeable: int
    :param general_score: int
    :param next_lecture: int
    :return: Boolean
    """
    today = get_today()
    lectures = models.Lecture.query.filter_by(subject=subject_name, year=today[0],
                                              week_number=today[1], day_number=today[2])
    try:
        feedback = models.LectureFeedbackEvaluation(user_name, lectures[0].id, increased_knowledge,
                                                    well_organized, use_of_slides, use_of_time,
                                                    presenter_knowledgeable, general_score, next_lecture)
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
    :param user_name: String
    :param lecture: int
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


def get_day():
    """
    :return day: int
    """
    return datetime.datetime.today().weekday() + 1


def get_week():
    """
    :return week: int
    """
    date = datetime.date.today()
    return datetime.date.isocalendar(date)[1]


def get_year():
    """
    :return year: int
    """
    date = datetime.date.today()
    return date.year


def get_lecture_object(lecture_id):
    """
    :param lecture_id: int
    :return lecture: query object
    """
    try:
        return models.Lecture.query.get(lecture_id)
    except Exception as e:
        print(e)
