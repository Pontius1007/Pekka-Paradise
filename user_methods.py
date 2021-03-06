from app import db, models


def has_user(user_name):
    """
    check if user in UserFacebook exists
    :param user_name:
    :return:
    """
    try:
        if models.UserFacebook.query.get(user_name) is not None:
            return True
        return False
    except Exception as e:
        print(e)


def add_user(user_name, subject_name):
    """
    Add a user and subject to UserFacebook
    Also adds subject to Subject-table if it is not present.
    :param user_name:
    :param subject_name:
    """
    try:
        subject_name = subject_name.upper()  # Subject names in the database should be uppercase
        if not subject_has_subject(subject_name):
            add_subject_to_subject_table(subject_name)
        if not has_user(user_name):
            new_user = models.UserFacebook(user_name, subject_name)
            db.session.add(new_user)
            db.session.commit()
        else:
            print('User already exists')
    except Exception as e:
        print(e)


def add_subject(user_name, subject_name):
    """
    Add subject to UserFacebook
    Also adds subject to Subject-table if it is not present.
    :param user_name:
    :param subject_name:
    """
    try:
        subject_name = subject_name.upper()  # Subject names in the database should be uppercase
        if not subject_has_subject(subject_name):
            add_subject_to_subject_table(subject_name)
        if models.UserFacebook.query.get(user_name) is None:
            add_user(user_name, subject_name)
        else:
            user = models.UserFacebook.query.get(user_name)
            user.subject = subject_name
            db.session.add(user)
            db.session.commit()
    except Exception as e:
        print(e)


def get_subject_from_user(user_name):
    """
    get subject from UserFacebook
    :param user_name:
    :return: subject_name
    """
    try:
        if models.UserFacebook.query.get(user_name) is not None:
            return models.UserFacebook.query.get(user_name).subject
    except Exception as e:
        print(e)
    return None


def delete_user(user_name):
    """
    deletes a user in UserFacebook table
    :param user_name:
    """
    if models.UserFacebook.query.get(user_name) is not None:
        for row in models.UserFacebook.query.filter_by(user_id=user_name):
            db.session.delete(row)
        db.session.commit()


def add_subject_to_subject_table(subject_name):
    """
    Adds subject to Subject-table
    :param subject_name:
    """
    try:
        subject = models.Subject(subject_name)
        db.session.add(subject)
        db.session.commit()
    except Exception as e:
        print(e)


def subject_has_subject(subject_name):
    """

    :param subject_name:
    :return: Boolean
    """
    try:
        if models.Subject.query.get(subject_name.upper()) is not None:
            return True
    except Exception as e:
        print(e)
    return False


def remove_subject(subject_name):
    """
    This method is only used for testing, and is used to
    remove dummy subject from db
    :param subject_name: String
    """
    for row in models.Subject.query.filter_by(subject_id=subject_name):
        db.session.delete(row)
    db.session.commit()
