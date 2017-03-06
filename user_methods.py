from app import db, models


def has_user(user_name):
    try:
        if models.UserFacebook.query.get(user_name) is not None:
            return True
    except Exception as e:
        print(e)
    return False


def add_user(user_name, subject_name):
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


add_user('Anders Larsen', 'TDT4110')
