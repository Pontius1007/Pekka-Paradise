from app import db, models


def add_entry(user_name, subject_name, feedback):
    """
    add feedback and course to table
    :param user_name:
    :param subject_name:
    :param feedback:
    """
    try:
        new_feedb = models.LectureFeedback(user_name, subject_name, feedback)
        db.session.add(new_feedb)
        db.session.commit()

    except Exception as e:
        print(e)
