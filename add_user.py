from app import db, models


def add_user(user_name, subject_name):
    try:
        new_user = models.UserFacebook(user_name, subject_name)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print(e)
