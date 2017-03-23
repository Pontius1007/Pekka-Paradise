# -*- coding utf-8 -*-

from app import db, models


def add_lecture_information_db(lecture_information):
    """
    :param lecture_information:
    :return: adds the corrects lectures in the database for the current subject
    """

    for i in range(0, len(lecture_information)):
        week_number = ''.join((lecture_information[i][4][0]))
        if len(week_number) > 2:
            start_week = int((week_number.split('-', 2)[0]))
            end_week = int((week_number.split('-', 2)[1]))
            year = lecture_information[i][5][:4]
            for x in range(start_week, end_week + 1):
                new_lecture = models.Lecture(lecture_information[i][0], year, x, lecture_information[i][3],
                                             lecture_information[i][1], lecture_information[i][2],
                                             lecture_information[i][6])
                db.session.add(new_lecture)
        else:
            year = lecture_information[i][5][:4]
            new_lecture_under_2 = models.Lecture(lecture_information[i][0], year, week_number,
                                                 lecture_information[i][3],
                                                 lecture_information[i][1],
                                                 lecture_information[i][2], lecture_information[i][6])
            db.session.add(new_lecture_under_2)
    db.session.commit()
    print("Lectures added successfully")


def check_lecture_in_db(subject):
    """
    :param subject:
    :return: True or False depending if the subject has any lectures in the database or not.
    False if no lectures are found
    """
    list_test = []
    # TODO Do this a better way
    for lecture in models.Lecture.query.filter_by(subject=subject):
        list_test.append(lecture)

    if len(list_test) == 0:
        return False
    else:
        return True


def get_lectures_from_subject(subject):
    """
    Checks if the subject is in db and returns list of id for all lectures
    :param subject:
    :return: A list of lecture ids for a subject
    """
    lecture_ids = []
    for lecture in models.Lecture.query.filter_by(subject=subject):
        print(lecture)
        lecture_ids.append(lecture.id)
    return lecture_ids


def get_lecture_from_date(year, week, day):
    """
    Gets lecture id from year, week and day
    :param year: int
    :param week: int
    :param day: int
    :return: lecture id, int
    """
    lectures = models.Lecture.query.filter_by(year=year, week_number=week, day_number=day)
    if lectures.count():
        lecture_id = lectures[0].id
        return lecture_id
