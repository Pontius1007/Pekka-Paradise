from app import db, models


def has_user(user_name):
    """
    check if user in userfacebook exists
    :param user_name:
    :return:
    """
    try:
        if models.UserFacebook.query.get(user_name) is not None:
            return True
    except Exception as e:
        print(e)
    return False


def add_user(user_name, subject_name):
    """
    add a user and subject to userfacebook
    :param user_name:
    :param subject_name:
    """
    subject_name = subject_name.upper()  # Subject names in the database should be uppercase
    try:
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
    add subject to userfacebook
    :param user_name:
    :param subject_name:
    """
    subject_name = subject_name.upper()  # Subject names in the database should be uppercase
    try:
        if models.UserFacebook.query.get(user_name) is None:
            add_user(user_name, subject_name)
        else:
            user = models.UserFacebook.query.get(user_name)
            user.subject = subject_name
            db.session.add(user)
            db.session.commit()
    except Exception as e:
        print(e)


def get_subject(user_name):
    """
    get subject from userfacebook
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
    deletes a user in userfacebook
    :param user_name:
    """
    if models.UserFacebook.query.get(user_name) is not None:
        db.session.delete(models.UserFacebook.query.get(user_name))
        db.session.commit()
