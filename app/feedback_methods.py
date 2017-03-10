from app import db, models


def add_entry(user_name, subject_name, feedback):
    """
    add feedback and course to table
    :param user_name:
    :param subject_name:
    :param feedback:
    """
    try:
        if check_entry(user_name, subject_name, feedback):
            new_feedb = models.LectureFeedback(user_name, subject_name, feedback)
            db.session.add(new_feedb)
            db.session.commit()
        else:
            print("User has already given feedback to this course")
    except Exception as e:
        print(e)


def check_entry(user_name, subject_name, feedback):
    try:
        # db.users.filter(or_(db.users.name=='Ryan', db.users.country=='England'))
        if models.LectureFeedback.query.filter(models.LectureFeedback.user_id == user_name and
                                               models.LectureFeedback.subject == subject_name) is None:
            return True  # Go for it add to db
    except Exception as e:
        print(e)
    return False
